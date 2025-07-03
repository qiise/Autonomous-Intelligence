from flask import Flask, request, jsonify, abort, redirect, send_file
from flask_cors import CORS, cross_origin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3
from api_endpoints.login.handler import LoginHandler, SignUpHandler, ForgotPasswordHandler, ResetPasswordHandler
import os
import pathlib
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
from flask.wrappers import Response
import json
import jwt
import requests
from database.db_auth import api_key_access_invalid
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, decode_token, JWTManager
from flask_mail import Mail
from jwt import InvalidTokenError
from urllib.parse import urlparse
from database.db import create_user_if_does_not_exist
from constants.global_constants import kSessionTokenExpirationTime
from database.db_auth import extractUserEmailFromRequest, is_session_token_valid, is_api_key_valid, user_id_for_email, verifyAuthForPaymentsTrustedTesters, verifyAuthForCheckoutSession, verifyAuthForPortalSession
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request
from api_endpoints.payments.handler import CreateCheckoutSessionHandler, CreatePortalSessionHandler, StripeWebhookHandler
from api_endpoints.refresh_credits.handler import RefreshCreditsHandler
from api_endpoints.user.handler import ViewUserHandler
from api_endpoints.generate_api_key.handler import GenerateAPIKeyHandler
from api_endpoints.delete_api_key.handler import DeleteAPIKeyHandler
from api_endpoints.get_api_keys.handler import GetAPIKeysHandler
from enum import Enum
import stripe
from dotenv import load_dotenv
import ray
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from flask_socketio import SocketIO, emit, disconnect
from database.db_auth import user_email_for_session_token
from flask.cli import with_appcontext
import click
import threading
import time
import csv
from fpdf import FPDF
import openai
import shutil
from io import BytesIO
import io
from tika import parser as p
import anthropic
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from datasets import Dataset
import re
import ragas
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)
from bs4 import BeautifulSoup

#WESLEY
from backend.api_endpoints.financeGPT.chatbot_endpoints import create_chat_shareable_url, access_sharable_chat


from api_endpoints.financeGPT.chatbot_endpoints import add_prompt_to_workflow_db, add_workflow_to_db, \
    add_chat_to_db, add_message_to_db, chunk_document, get_text_from_single_file, add_document_to_db, get_relevant_chunks,  \
    remove_prompt_from_workflow_db, remove_ticker_from_workflow_db, reset_uploaded_docs_for_workflow, retrieve_chats_from_db, \
    delete_chat_from_db, retrieve_message_from_db, retrieve_docs_from_db, add_sources_to_db, delete_doc_from_db, reset_chat_db, change_chat_mode_db, update_chat_name_db, \
    add_ticker_to_chat_db, download_10K_url_ticker, download_filing_as_pdf, reset_uploaded_docs, check_valid_api, add_model_key_to_db, get_text_pages_from_single_file, \
    add_ticker_to_workflow_db, add_chat_to_db, add_message_to_db, chunk_document, get_text_from_single_file, add_document_to_db, get_relevant_chunks, process_ticker_info_wf, \
    retrieve_chats_from_db, delete_chat_from_db, retrieve_message_from_db, retrieve_docs_from_db, add_sources_to_db, delete_doc_from_db, reset_chat_db, \
    change_chat_mode_db, update_chat_name_db, find_most_recent_chat_from_db, process_prompt_answer, \
    ensure_SDK_user_exists, get_chat_info, ensure_demo_user_exists, get_message_info, get_text_from_url, \
    add_organization_to_db, get_organization_from_db

from datetime import datetime

load_dotenv(override=True)

app = Flask(__name__)

if ray.is_initialized() == False:
  ray.init(logging_level="INFO", log_to_driver=True)

# TODO: Replace with your URLs.
config = {
  'ORIGINS': [
    'http://localhost:3000',  # React
    'http://dashboard.localhost:3000',  # React
    'https://anote.ai', # Frontend prod URL,
    'https://privatechatbot.ai', # Frontend prod URL,
    'https://dashboard.privatechatbot.ai', # Frontend prod URL,
  ],
}
CORS(app, resources={ r'/*': {'origins': config['ORIGINS']}}, supports_credentials=True)

app.secret_key = '6cac159dd02c902f822635ee0a6c3078'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config["JWT_SECRET_KEY"] = "6cac159dd02c902f822635ee0a6c3078"
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = kSessionTokenExpirationTime
app.config["JWT_TOKEN_LOCATION"] = "headers"
app.config.from_object(__name__)

jwt_manager = JWTManager(app)
app.jwt_manager = jwt_manager

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vidranatan@gmail.com'
app.config['MAIL_PASSWORD'] = 'fhytlgpsjyzutlnm'
app.config['MAIL_DEFAULT_SENDER'] = 'vidranatan@gmail.com'
mail = Mail(app)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def valid_api_key_required(fn):
  @wraps(fn)
  def wrapper(*args, **kwargs):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        splits = auth_header.split(' ')
        if len(splits) > 1:
          api_key = auth_header.split(' ')[1]
          if is_api_key_valid(api_key):
            # If api key is valid, return the decorated function
            return fn(*args, **kwargs)
    # If API key is not present or valid, return an error message or handle it as needed
    return "Unauthorized", 401
  return wrapper

def jwt_or_session_token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
      return fn(*args, **kwargs)
    return wrapper


class ProtectedDatabaseTable(Enum):
    # PROFILE_LISTS = 1
    # PROFILES_MULTI = 2
    API_KEYS = 1

# Example of auth function.  This would be called like
# verifyAuthForIDs(ProtectedDatabaseTable.PROFILE_LISTS, request.json["id"])
# in your flask endpoints before calling business logic.  This needs to
# be modified to fit your schema.
def verifyAuthForIDs(table, non_user_id):
  try:
    user_email = extractUserEmailFromRequest(request)
  except InvalidTokenError:
    # If the JWT is invalid, return an error
    return jsonify({"error": "Invalid JWT"}), 401

  access_denied = False
  user_id = user_id_for_email(user_email)
  if table == ProtectedDatabaseTable.API_KEYS:
    access_denied = api_key_access_invalid(user_id, non_user_id)
  if access_denied:
    abort(401)

#WESLEY
@app.route('/generate-playbook/<string:chat_id>', methods = ["GET"])
@jwt_or_session_token_required
def create_shareable_playbook(chat_id):
    return create_chat_shareable_url(chat_id)
@app.route('/playbook/<string:playbook_url>', methods=["POST"])
@cross_origin(supports_credentials=True)
def import_shared_chat(playbook_url):
    return access_sharable_chat(playbook_url) 
@app.route('/health', methods=['GET'])
def health_check():
    return "Healthy", 200

# Auth
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  #this is to set our environment to https because OAuth 2.0 only supports https environments

GOOGLE_CLIENT_ID = "261908856206-fff63nag7j793tkbapd3hugthbcp8kfn.apps.googleusercontent.com"  #enter your client id you got from Google console
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")  #set the path to where the .json file you got Google console is

flow = Flow.from_client_secrets_file(  #Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
    client_secrets_file=client_secrets_file,
    # scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/gmail.send", "openid"],  #here we are specifing what do we get after the authorization
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  #here we are specifing what do we get after the authorization
    # redirect_uri="http://localhost:5000/callback"  #and the redirect URI is the point where the user will end up after the authorization
    # redirect_uri="http://127.0.0.1:3000"  #and the redirect URI is the point where the user will end up after the authorization
)
# postmessage

@app.route("/login")  #the page where the user can login
@cross_origin(supports_credentials=True)
def login():
    if request.args.get('email') and len(request.args.get('email')) > 0:
      return LoginHandler(request)
    else:
      o = urlparse(request.base_url)
      netloc = o.netloc
      scheme = "https"
      if "localhost" in netloc:
        scheme = "http"
    
      flow.redirect_uri = f'{scheme}://{netloc}/callback'
    #   flow.redirect_uri = f'https://upreachapi.upreach.ai/callback'

      state_dict = {
        "redirect_uri": flow.redirect_uri
      }

      if request.args.get('product_hash'):
        print("during checking product hash")
        state_dict["product_hash"] = request.args.get('product_hash')
      if request.args.get('free_trial_code'):
        print("during checking free_trial_code")
        state_dict["free_trial_code"] = request.args.get('free_trial_code')

      state = jwt.encode(state_dict, app.config["JWT_SECRET_KEY"], algorithm="HS256")

      # Generate the authorization URL and use the JWT as the state value
      authorization_url, _ = flow.authorization_url(state=state)

      response = Response(
          response=json.dumps({'auth_url':authorization_url}),
          status=200,
          mimetype='application/json'
      )
      response.headers.add('Access-Control-Allow-Headers',
                          'Origin, Content-Type, Accept')
      return response



@app.route("/callback")  #this is the page that will handle the callback process meaning process after the authorization
@cross_origin(supports_credentials=True)
def callback():
    try:
        decrypted_token = jwt.decode(request.args["state"], app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        product_hash = decrypted_token.get('product_hash', None)
        free_trial_code = decrypted_token.get('free_trial_code', None)
    except jwt.exceptions.InvalidSignatureError:
        abort(500)
    flow.redirect_uri = decrypted_token["redirect_uri"]
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    # TODO: COMMENT OUT WHEN DEPLOY TO PROD
    default_referrer = "http://dashboard.localhost:3000"
    # default_referrer = "https://dashboard.privatechatbot.ai"
    user_id = create_user_if_does_not_exist(id_info.get("email"), id_info.get("sub"), id_info.get("name"), id_info.get("picture"))

    access_token = create_access_token(identity=id_info.get("email"))
    refresh_token = create_refresh_token(identity=id_info.get("email"))
    productGetParam = ""
    if product_hash is not None:
      productGetParam = "&" + "product_hash=" + product_hash
    freeTrialCodeGetParam = ""
    if free_trial_code is not None:
      freeTrialCodeGetParam = "&" + "free_trial_code=" + free_trial_code

    print("request.referrer")
    print(request.referrer)
    # response = redirect(
    #   (request.referrer or default_referrer) +
    #   "?accessToken=" + access_token + "&"
    #   "refreshToken=" + refresh_token
    # )
    response = redirect(
      (default_referrer) +
      "?accessToken=" + access_token + "&"
      "refreshToken=" + refresh_token + productGetParam + freeTrialCodeGetParam
    )
    return response

# This route is used to refresh the JWT
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    # Get the JWT refresh token from the Authorization header
    authorization_header = request.headers["Authorization"]
    authorization_header_parts = authorization_header.split(" ")

    if len(authorization_header_parts) >= 2:
      jwt_token = authorization_header_parts[1]

      try:
          # Try to decode the JWT
          decoded_jwt = decode_token(jwt_token)

          # If the JWT is valid, generate a new JWT with a refreshed expiration time
          access_token = create_access_token(identity=decoded_jwt["sub"])

          # Return the new JWT in the response
          return jsonify({"accessToken": access_token}), 200
      except InvalidTokenError:
          # If the JWT is invalid, return an error
          return jsonify({"error": "Invalid JWT"}), 401
    else:
      # If the Authorization header does not have enough elements, return an error
        return jsonify({"error": "Invalid Authorization header"}), 401

@app.route("/signUp", methods=["POST"])
@cross_origin(supports_credentials=True)
def signUp():
  return SignUpHandler(request)

@app.route("/forgotPassword", methods=["POST"])
@cross_origin(supports_credentials=True)
def forgotPassword():
  return ForgotPasswordHandler(request, mail)

@app.route("/resetPassword", methods=["POST"])
@cross_origin(supports_credentials=True)
def resetPassword():
  return ResetPasswordHandler(request)

@app.route('/refreshCredits', methods = ['POST'])
@jwt_or_session_token_required
def RefreshCredits():
  try:
    user_email = extractUserEmailFromRequest(request)
  except InvalidTokenError:
    # If the JWT is invalid, return an error
    return jsonify({"error": "Invalid JWT"}), 401
  return jsonify(RefreshCreditsHandler(request, user_email))

# Billing

@app.route('/createCheckoutSession', methods=['POST'])
@jwt_or_session_token_required
def create_checkout_session():
  try:
    user_email = extractUserEmailFromRequest(request)
  except InvalidTokenError:
    # If the JWT is invalid, return an error
    return jsonify({"error": "Invalid JWT"}), 401
  if not verifyAuthForPaymentsTrustedTesters(user_email):
    abort(401)
  verifyAuthForCheckoutSession(user_email, mail)
  return CreateCheckoutSessionHandler(request, user_email)

@app.route('/createPortalSession', methods=["POST"])
@jwt_or_session_token_required
def customer_portal():
  try:
    user_email = extractUserEmailFromRequest(request)
  except InvalidTokenError:
    # If the JWT is invalid, return an error
    return jsonify({"error": "Invalid JWT"}), 401
  print("got email customer_portal")
  if not verifyAuthForPaymentsTrustedTesters(user_email):
    print("no verifyAuthForPaymentsTrustedTesters")
    abort(401)
  verifyAuthForPortalSession(request, user_email, mail)
  return CreatePortalSessionHandler(request, user_email)

STRIPE_WEBHOOK_SECRET = "whsec_Ustl52CpxewYc33WdamF06lDCjgg3a2e"

@app.route('/stripeWebhook', methods=['POST'])
def stripe_webhook():
  sig_header = request.headers.get('Stripe-Signature')
  try:
      # Verify the signature of the event
      event = stripe.Webhook.construct_event(
          request.data, sig_header, STRIPE_WEBHOOK_SECRET
      )
  except (stripe.error.SignatureVerificationError, ValueError):
      return 'Invalid signature', 400
  return StripeWebhookHandler(request, event)

@app.route('/viewUser', methods = ['GET'])
@jwt_or_session_token_required
def ViewUser():
  try:
    user_email = extractUserEmailFromRequest(request)
  except InvalidTokenError:
    # If the JWT is invalid, return an error
    return jsonify({"error": "Invalid JWT"}), 401
  return ViewUserHandler(request, user_email)

# Example of a background task that can consistently do
# some processing in the background independently of your
# actual web app.
# def background_task():
#   try:
#     print("inside background task")
#     with app.app_context():  # This is important to access Flask app resources
#       while True:
#         automation_ids = view_automations_to_process()
#         print("automation_ids", automation_ids)
#         for id in automation_ids:
#           print("in for automation_ids")
#           socketId = get_socket_for_automation(id)
#           print("socketId")
#           print(socketId)
#           trigger_automation_step.remote(id, auth, host, socketId)
#         time.sleep(60)
#   except Exception as e:
#     print(f"Exception in background_task: {e}")
# app.start_background_task(background_task)

# Helper function to scrape sub-URLs from the main website
def get_links(initial_url: str):
    # Send a GET request to the website's URL
    response = requests.get(initial_url)

    # Parse the HTML code with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> tags and extract the href attribute (the hyperlink)
    links = []
    links_text = []
    for link in soup.find_all('a'):
        if type(link.get('href')) == str:
            if link.get('href')[0] == "/":
                web_url = initial_url.rstrip("/") + link.get('href')  # Full URL
                web_text = get_text_from_url(web_url)
                if len(web_text) > 0:
                    links.append(web_url)
                    links_text.append(web_text)
    return links, links_text

# Helper function to extract text from a URL
def get_text_from_url(web_url):
    response = requests.get(web_url)
    result = p.from_buffer(response.content)
    text = result.get("content", "").strip()
    return text.replace("\n", "").replace("\t", "")

# Organization routes

@app.route('/create_organization', methods=['POST'])
@valid_api_key_required
def create_organization():
    try:
        name = request.json.get('name')
        organization_type = request.json.get('organization_type')  # 'enterprise' or 'individual'
        website_url = request.json.get('website_url')

        if not name or not organization_type:
            return jsonify({"error": "Missing required fields"}), 400

        # Add organization to the database
        organization_id = add_organization_to_db(name, organization_type, website_url)

        # Scrape website if a URL is provided
        if website_url:
            print(f"Scraping website {website_url}...")
            links, links_text = get_links(website_url)
            for link, link_text in zip(links, links_text):
                print(f"Processing scraped URL {link}...")
                # Ingest each sub-URL's text as a document
                doc_id, doesExist = add_document_to_db(link_text, link, organization_id)
                if not doesExist:
                    chunk_document.remote(link_text, 1000, doc_id)

        return jsonify({"organization_id": organization_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_organization', methods=['GET'])
@valid_api_key_required
def get_organization():
    try:
        organization_id = request.args.get('organization_id')
        if not organization_id:
            return jsonify({"error": "Missing organization_id"}), 400

        # Get organization info from the database
        organization = get_organization_from_db(organization_id)
        if not organization:
            return jsonify({"error": "Organization not found"}), 404

        return jsonify(organization), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/<organization_name>')
def chat_with_organization(organization_name):
    organization = get_organization_from_db_by_name(organization_name)
    if organization:
        return jsonify({
            'name': organization['name'],
            'website_url': organization['website_url'],
            'organization_type': organization['organization_type']
        })
    else:
        return jsonify({'error': 'Organization not found'}), 404

def get_organization_from_db_by_name(organization_name):
    conn, cursor = get_db_connection()
    cursor.execute('SELECT * FROM organizations WHERE name = %s', [organization_name])
    organization = cursor.fetchone()
    conn.close()
    return organization

## CHATBOT SECTION
output_document_path = 'output_document'
chat_history_file = os.path.join(output_document_path, 'chat_history.csv')
vector_base_path = 'db'
source_documents_path = 'source_documents'

@app.route('/api/reset-everything', methods=['POST']) #Change this to use MYSQL db
def reset_everything():
    try:
        # Delete vector database
        #shutil.rmtree(vector_base_path)
        # Delete user input documents
        if os.path.exists(source_documents_path):
            shutil.rmtree(source_documents_path)
        # Delete chat history
        if os.path.exists(output_document_path):
            shutil.rmtree(output_document_path)
            # Recreate the output folder
            os.makedirs(output_document_path)

        # Create an empty chat history CSV file
        chat_history_file_path = os.path.join(output_document_path, 'chat_history.csv')
        with open(chat_history_file_path, 'w', newline='') as csvfile:
            print("test1")
            writer = csv.writer(csvfile)
            writer.writerow(['query', 'response'])

        return 'Reset was successful!'
    except Exception as e:
        return f'Failed to delete DB folder: {str(e)}', 500

@app.route('/download-chat-history', methods=['POST'])
def download_chat_history():
    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
        # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    try:
        chat_type = request.json.get('chat_type')
        chat_id = request.json.get('chat_id')

        messages = retrieve_message_from_db(user_email, chat_id, chat_type)

        paired_messages = []

        for i in range(len(messages) - 1):
            if messages[i]['sent_from_user'] == 1 and messages[i+1]['sent_from_user'] == 0:
                regex = re.compile(r"Document:\s*[^:]+:\s*(.*?)(?=Document:|$)", re.DOTALL)
                if messages[i+1]["relevant_chunks"]:
                    found = re.findall(regex, messages[i+1]["relevant_chunks"])
                    paragraphs = [paragraph.strip() for paragraph in found]
                    if len(paragraphs) > 1:
                        paired_messages.append((messages[i]['message_text'], messages[i+1]['message_text'], paragraphs[0], paragraphs[1]))
                    elif len(paragraphs) == 1:
                        paired_messages.append((messages[i]['message_text'],  messages[i+1]['message_text'], paragraphs[0], None))
                else:
                    paired_messages.append((messages[i]['message_text'], messages[i+1]['message_text'], None, None))


        csv_output = io.StringIO()
        writer = csv.writer(csv_output)
        writer.writerow(['query', 'response', 'chunk1', 'chunk2'])  # Write header
        writer.writerows(paired_messages)
        csv_output.seek(0)  # Go back to the start of the StringIO object

        return Response(
            csv_output.getvalue(),
            mimetype='text/csv',
            headers={"Content-disposition": "attachment; filename=chat_history.csv"}
        )
    except Exception as e:
        print("error is,", str(e))
        return jsonify({"error": str(e)}), 500




@app.route('/create-new-chat', methods=['POST'])
def create_new_chat():
    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    chat_type = request.json.get('chat_type')
    model_type = request.json.get('model_type')

    chat_id = add_chat_to_db(user_email, chat_type, model_type) #for now hardcode the model type as being 0

    return jsonify(chat_id=chat_id)

@app.route('/retrieve-all-chats', methods=['POST'])
def retrieve_chats():
    #Given an input of a chat_type and user_email, it will return as a list of dictionaries all the chats of that user and chat type from the db

    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401
    #chat_type = request.json.get('chat_type')

    chat_info = retrieve_chats_from_db(user_email)

    return jsonify(chat_info=chat_info)

@app.route('/retrieve-messages-from-chat', methods=['POST'])
def retrieve_messages_from_chat():
    #Getting current user not working, fix this later
    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    chat_type = request.json.get('chat_type')
    chat_id = request.json.get('chat_id')

    messages = retrieve_message_from_db(user_email, chat_id, chat_type)

    return jsonify(messages=messages)


@app.route('/update-chat-name', methods=['POST'])
def update_chat_name():
    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    chat_name = request.json.get('chat_name')
    chat_id = request.json.get('chat_id')

    print("chat_name", chat_name)

    update_chat_name_db(user_email, chat_id, chat_name)

    return jsonify({"Success": "Chat name updated"}), 200

@app.route('/infer-chat-name', methods=['POST'])
def infer_chat_name():
    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    chat_messages = request.json.get('messages')
    chat_id = request.json.get('chat_id')

    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user",
             "content": f"Based off these 2 messages between me and my chatbot, please infer a name for the chat. Keep it to a maximum of 4 words, 5 if you must. Do not use the word chat in it. Some good examples are, AI research paper, Apple financial report, Questions about earnings calls. Return only the chatname and nothing else. Here are the messages: {chat_messages}"}
        ]
    )
    new_name = str(completion.choices[0].message.content)

    update_chat_name_db(user_email, chat_id, new_name)

    return jsonify(chat_name=new_name)

@app.route('/update-workflow-name', methods=['POST'])
def update_workflow_name():
    print("Print Update-Workflow-Name")
    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    workflow_name = request.json.get('workflow_name')
    workflow_id = request.json.get('workflow_id')

    print("NEW workflow_name", workflow_name)

    update_workflow_name_db(user_email, workflow_id, workflow_name)

    return "Workflow name updated"


@app.route('/delete-chat', methods=['POST'])
def delete_chat():
    chat_id = request.json.get('chat_id')

    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    return delete_chat_from_db(chat_id, user_email)


@app.route('/find-most-recent-chat', methods=['POST'])
def find_most_recent_chat():
    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    chat_info = find_most_recent_chat_from_db(user_email)

    return jsonify(chat_info=chat_info)


@app.route('/ingest-pdf', methods=['POST'])
def ingest_pdfs():
    start_time = datetime.now()
    print("start time is", start_time)

    chat_id = request.form.getlist('chat_id')[0]
    files = request.files.getlist('files[]')

    MAX_CHUNK_SIZE = 1000

    print("before files loop time is", datetime.now() - start_time)
    for file in files:
        #text = get_text_from_single_file(file)
        #text_pages = get_text_pages_from_single_file(file)

        result = p.from_buffer(file)
        text = result["content"].strip()

        filename = file.filename

        doc_id, doesExist = add_document_to_db(text, filename, chat_id=chat_id)

        if not doesExist:
           chunk_document.remote(text, MAX_CHUNK_SIZE, doc_id)


    return jsonify({"error": "Invalid JWT"}), 200


    #return text, filename

@app.route('/api/ingest-pdf-wf', methods=['POST'])
def ingest_pdfs_wf():
    workflow_id = request.form['workflow_id']

    if 'files' not in request.files:
        return "No file part in the request", 400

    files = request.files.getlist('files')

    MAX_CHUNK_SIZE = 1000

    for file in files:
        text = get_text_from_single_file(file)
        text_pages = get_text_pages_from_single_file(file)
        filename = file.filename

        text
        doc_id, doesExist = add_document_to_db(text, filename, workflow_id)

        if not doesExist:
          chunk_document.remote(text_pages, MAX_CHUNK_SIZE, doc_id)
    return text, filename

@app.route('/retrieve-current-docs', methods=['POST'])
def retrieve_current_docs():
    chat_id = request.json.get('chat_id')

    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    doc_info = retrieve_docs_from_db(chat_id, user_email)

    return jsonify(doc_info=doc_info)

@app.route('/delete-doc', methods=['POST'])
def delete_doc():
    doc_id = request.json.get('doc_id')

    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    delete_doc_from_db(doc_id, user_email)

    return "success"

@app.route('/change-chat-mode', methods=['POST'])
def change_chat_mode_and_reset_chat():
    chat_mode_to_change_to = request.json.get('model_type')
    chat_id = request.json.get('chat_id')

    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    try:
        reset_chat_db(chat_id, user_email)
        change_chat_mode_db(chat_mode_to_change_to, chat_id, user_email)

        return "Success"
    except:
        return "Error"

@app.route('/reset-chat', methods=['POST'])
def reset_chat():
    chat_id = request.json.get('chat_id')
    delete_docs = request.json.get('delete_docs')

    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    if delete_docs:
        reset_uploaded_docs(chat_id, user_email)

    reset_chat_db(chat_id, user_email)

    return jsonify({"Success": "Success"}), 200

@app.route('/process-message-pdf', methods=['POST'])
def process_message_pdf():
    message = request.json.get('message')
    chat_id = request.json.get('chat_id')
    model_type = request.json.get('model_type')
    model_key = request.json.get('model_key')


    is_guest = chat_id == 0

    if not is_guest:
        try:
            user_email = extractUserEmailFromRequest(request)
        except InvalidTokenError:
        # If the JWT is invalid, return an error
            return jsonify({"error": "Invalid JWT"}), 401

        ##Include part where we verify if user actually owns the chat_id later
    else:
        user_email = "guest@gmail.com"
    query = message.strip()

    #This adds user message to db
    if not is_guest:
        add_message_to_db(query, chat_id, 1)

    #Get most relevant section from the document
    if not is_guest:
        sources = get_relevant_chunks(2, query, chat_id, user_email)
    else: 
        sources = []
    
    sources_str = " ".join([", ".join(str(elem) for elem in source) for source in sources])

    if (model_type == 0):
        if model_key:
           model_use = model_key
        else:
           model_use = "gpt-4o-mini"

        print("using OpenAI and model is", model_use)
        client = openai.OpenAI()
        try:
            completion = client.chat.completions.create(
                model=model_use,
                messages=[
                    {"role": "user",
                     "content": f"You are a factual chatbot that answers questions about uploaded documents. You only answer with answers you find in the text, no outside information. These are the sources from the text:{sources_str} And this is the question:{query}."}
                ]
            )
            print("using fine tuned model")
            answer = str(completion.choices[0].message.content)
        except openai.NotFoundError:
            print(f"The model `{model_use}` does not exist. Falling back to 'gpt-4'.")
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user",
                     "content": f"First, tell the user that their given model key does not exist, and that you have resorted to using GPT-4 before answering their question, then add a line break and answer their question. You are a factual chatbot that answers questions about uploaded documents. You only answer with answers you find in the text, no outside information. These are the sources from the text:{sources[0]}{sources[1]} And this is the question:{query}."}
                ]
            )
            answer = str(completion.choices[0].message.content)
    else:
        print("using Claude")

        anthropic = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

        completion = anthropic.completions.create(
            model="claude-2",
            max_tokens_to_sample=700,
            prompt = (
              f"{HUMAN_PROMPT} "
              f"You are a factual chatbot that answers questions about uploaded documents. You only answer with answers you find in the text, no outside information. "
              f"please address the question: {query}. "
              f"Consider the provided text as evidence: {sources_str}. "
              f"{AI_PROMPT}")
        )
        answer = completion.completion

    #This adds bot message
    message_id = None
    if not is_guest:
        message_id = add_message_to_db(answer, chat_id, 0)
        if message_id:

            try:
                add_sources_to_db(message_id, sources)
            except:
                print("no sources")

    return jsonify(answer=answer)

# Only for demo purposes
chat_to_document_mapping = {}
#DEMO_CHAT_ID = 99999
DEMO_USER_EMAIL = "demo@example.com"
chat_id = 0

@app.route('/process-message-pdf-demo', methods=['POST'])
def process_message_pdf_demo():
    message = request.json.get('message')
    query = message.strip()

    global chat_id
    user_email = DEMO_USER_EMAIL

    print("CHAT ID IS", chat_id)

    add_message_to_db(query, chat_id, 1)

    sources = get_relevant_chunks(2, query, chat_id, user_email)
    print('sources is', sources)
    sources_str = " ".join([", ".join(str(elem) for elem in source) for source in sources])
    print('sources_str is', sources_str)


    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user",
             "content": f"You are a factual chatbot that answers questions about uploaded documents. You only answer with answers you find in the text, no outside information. These are the sources from the text:{sources_str} And this is the question:{query}."}
        ]
    )
    answer = str(completion.choices[0].message.content)

    message_id = add_message_to_db(answer, chat_id, 0)

    try:
        add_sources_to_db(message_id, sources)
    except:
        print("no sources")

    return jsonify(answer=answer)


@app.route('/ingest-pdf-demo', methods=['POST'])
def ingest_pdfs_demo():
    global chat_id
    user_email = DEMO_USER_EMAIL

    #create_new_demo_chat(chat_id, user_email)

    files = request.files.getlist('files[]')
    MAX_CHUNK_SIZE = 1000

    for file in files:
        result = p.from_buffer(file)  # Ensure your PDF extraction works as expected
        text = result["content"].strip()
        filename = file.filename

        # Assuming add_document_to_db and chunk_document.remote are implemented
        doc_id, doesExist = add_document_to_db(text, filename, chat_id=chat_id)
        if not doesExist:
            chunk_document.remote(text, MAX_CHUNK_SIZE, doc_id)

    # This mapping is now redundant since we're using a static demo_chat_id, but you could maintain it if you plan to extend functionality
    chat_to_document_mapping[chat_id] = doc_id

    return jsonify({"message": "Document processed successfully"}), 200

# @app.route('/reset-chat-demo', methods=['POST'])
# def reset_chat_demo():
#     global chat_id
#     user_email = DEMO_USER_EMAIL

#     ensure_demo_user_exists(user_email)

#     delete_chat_from_db(chat_id, user_email)

#     #create_new_demo_chat(chat_id, user_email)
#     chat_id = add_chat_to_db(user_email, 0, 0)

#     #reset_uploaded_docs(chat_id, user_email)

#     #reset_chat_db(chat_id, user_email)

#     return jsonify({"Success": "Success"}), 200

@app.route('/download-chat-history-demo', methods=['POST'])
def download_chat_history_demo():
    global chat_id
    user_email = DEMO_USER_EMAIL

    try:
        chat_type = 0

        messages = retrieve_message_from_db(user_email, chat_id, chat_type)

        print("messages", messages)

        paired_messages = []
        for i in range(len(messages) - 1):
            if messages[i]['sent_from_user'] == 1 and messages[i+1]['sent_from_user'] == 0:
                regex = re.compile(r"Document:\s*[^:]+:\s*(.*?)(?=Document:|$)", re.DOTALL)
                if messages[i+1]["relevant_chunks"]:
                    found = re.findall(regex, messages[i+1]["relevant_chunks"])
                    paragraphs = [paragraph.strip() for paragraph in found]
                    if len(paragraphs) > 1:
                        paired_messages.append((messages[i]['message_text'], messages[i+1]['message_text'], paragraphs[0], paragraphs[1]))
                    elif len(paragraphs) == 1:
                        paired_messages.append((messages[i]['message_text'],  messages[i+1]['message_text'], paragraphs[0], None))
                else:
                    paired_messages.append((messages[i]['message_text'], messages[i+1]['message_text'], None, None))

        csv_output = io.StringIO()
        writer = csv.writer(csv_output)
        writer.writerow(['query', 'response', 'chunk1', 'chunk2'])
        writer.writerows(paired_messages)
        csv_output.seek(0)

        # Return the CSV content as a response
        return Response(
            csv_output.getvalue(),
            mimetype='text/csv',
            headers={"Content-disposition": "attachment; filename=chat_history.csv"}
        )
    except Exception as e:
        print("error is,", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/add-model-key', methods=['POST'])
def add_model_key():
    model_key = request.json.get('model_key')
    chat_id = request.json.get('chat_id')

    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    add_model_key_to_db(model_key, chat_id, user_email)

    return "success"


#Edgar
@app.route('/check-valid-ticker', methods=['POST'])
def check_valid_ticker():
   ticker = request.json.get('ticker')
   result = check_valid_api(ticker)
   return jsonify({'isValid': result})

@app.route('/add-ticker-to-chat', methods=['POST'])
def add_ticker():
    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    ticker = request.json.get('ticker')
    chat_id = request.json.get('chat_id')
    isUpdate = request.json.get('isUpdate')

    return add_ticker_to_chat_db(chat_id, ticker, user_email, isUpdate)


@app.route('/process-ticker-info', methods=['POST'])
def process_ticker_info():
    chat_id = request.json.get('chat_id')
    ticker = request.json.get('ticker')

    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    if ticker:
        MAX_CHUNK_SIZE = 1000

        reset_uploaded_docs(chat_id, user_email)


        url, ticker = download_10K_url_ticker(ticker)
        filename = download_filing_as_pdf(url, ticker)

        text = get_text_from_single_file(filename)

        #result = p.from_buffer(filename)
        #text = result["content"].strip()

        #
        #text_pages = get_text_pages_from_single_file(filename)

        print("test1")
        doc_id, doesExist = add_document_to_db(text, filename, chat_id)

        if not doesExist:
            print("test")
            chunk_document.remote(text, MAX_CHUNK_SIZE, doc_id)
            #remote_task = chunk_document.remote(text, MAX_CHUNK_SIZE, doc_id)
            #result = ray.get(remote_task)

        #if os.path.exists(filename):
        #    os.remove(filename)
        #    print(f"File '{filename}' has been deleted.")
        #else:
        #    print(f"The file '{filename}' does not exist.")


    return jsonify({"error": "Invalid JWT"}), 200



@app.route('/temp-test', methods=['POST'])
def temp_test():

    anthropic = Anthropic(
      api_key=os.getenv("ANTHROPIC_API_KEY")
    )


    query = "What are some of the risk factors from the company?"

    sources = ["The Company’s business, reputation, results of operations, financial condition and stock price can be affected by a number of factors, whether currently known or unknown, including those described below. When any one or more of these risks materialize from time to time, the Company’s business, reputation, results of operations, financial condition and stock price can be materially and adversely affected. Because of the following factors, as well as other factors affecting the Company’s results of operations and financial condition, past financial performance should not be considered to be a reliable indicator of future performance, and investors should not use historical trends to anticipate results or trends in future periods. This discussion of risk factors contains forward-looking statements. This section should be read in conjunction with Part II, Item 7, “Management’s Discussion and Analysis of Financial Condition and Results of Operations” and the consolidated financial statements and accompanying notes in Part II, Item 8, “Financial Statements and Supplementary Data” of this Form 10-K.", "The Company’s operations and performance depend significantly on global and regional economic conditions and adverse economic conditions can materially adversely affect the Company’s business, results of operations and financial condition. The Company has international operations with sales outside the U.S. representing a majority of the Company’s total net sales. In addition, the Company’s global supply chain is large and complex and a majority of the Company’s supplier facilities, including manufacturing and assembly sites, are located outside the U.S. As a result, the Company’s operations and performance depend significantly on global and regional economic conditions."]

    completion = anthropic.completions.create(
      model="claude-2",
      max_tokens_to_sample=700,
      prompt = (
        f"{HUMAN_PROMPT} "
        f"You are a factual chatbot that answers questions about 10-K documents. You only answer with answers you find in the text, no outside information. "
        f"please address the question: {query}. "
        f"Consider the provided text as evidence: {sources[0]}{sources[1]}. "
        f"{AI_PROMPT}")
    )

    print("anthropic result", completion.completion)

    return 'success'



## WORKFLOWS SECTION

@app.route('/create-new-workflow', methods=['POST'])
def create_new_workflow():
    print('create_new_workflow')
    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    workflow_type = request.json.get('workflow_type')
    model_type = request.json.get('model_type')

    workflow_id = add_workflow_to_db(user_email, workflow_type) #DO I NEED MODEL_TYPE
    print(f'Workflow_id is APP :', workflow_id)
    return jsonify(workflow_id=workflow_id)

@app.route('/remove-ticker-from-workflow', methods=['POST'])
def remove_ticker_from_workflow():
    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
        return jsonify({"error": "Invalid JWT"}), 401

    ticker = request.json.get('ticker')
    workflow_id = request.json.get('workflow_id')

    return remove_ticker_from_workflow_db(workflow_id, ticker, user_email)

@app.route('/add-prompt-to-workflow', methods=['POST'])
def add_prompt_to_workflow():
    try:
        user_email = extractUserEmailFromRequest(request)
        workflow_id = request.json.get('workflow_id')
        prompt_text = request.json.get('prompt_text')
    except InvalidTokenError:
        return jsonify({"error": "Invalid JWT"}), 401

    return add_prompt_to_workflow_db(workflow_id, prompt_text)

@app.route('/remove-prompt-from-workflow', methods=['POST'])
def remove_prompt_from_workflow():
    try:
        user_email = extractUserEmailFromRequest(request)
        prompt_id = request.json.get('prompt_id')
    except InvalidTokenError:
        return jsonify({"error": "Invalid JWT"}), 401

    return remove_prompt_from_workflow_db(prompt_id)




@app.route('/generate_financial_report', methods=['POST'])
def generate_financial_report():
    print("generate_financial_report")

    try:
        user_email = extractUserEmailFromRequest(request)
    except InvalidTokenError:
    # If the JWT is invalid, return an error
        return jsonify({"error": "Invalid JWT"}), 401

    try:
        tickers = request.json.get('tickers')
        print(f"tickers: {tickers}")
        questions = request.json.get('questions')
        workflowId = request.json.get('workflowId')

        # Initialize a single PDF for all tickers
        pdf = FPDF()
        pdf.add_page()

        pdf_title = '_'.join(tickers).upper()
        pdf_title = f'Financial_Report_{pdf_title}'
        pdf.set_title(pdf_title)

        for ticker in tickers:
            print(f"Processing ticker: {ticker}")
            pdf.set_font('Times', 'B', 16)
            pdf.ln(2)

            # Include standard header of company information in the PDF
            pdf.ln(h=5)
            pdf.set_font('Times', 'B', 12)
            pdf.write(1, f'Ticker: {ticker.upper()}')

            process_ticker_info_wf(user_email, workflowId, ticker)
            print("SUCCESSFULLY PROCESSED TICKER")

            # Including Q&A in PDF
            for question in questions:
                print(f"for loop")
                answer = process_prompt_answer(question, workflowId, user_email)
                print("Successfully processed answer: ", )
                answer_encoded = answer.encode('latin-1', 'replace').decode('latin-1')
                question_encoded = question.encode('latin-1', 'replace').decode('latin-1')

                pdf.ln(h=5)
                pdf.set_font('Times', 'B', 12)
                pdf.write(1, question_encoded)
                pdf.set_font('Times', '', 12)
                pdf.ln(h=5)
                pdf.multi_cell(0, 5, answer_encoded)
                print("PRINTED Q&A")

        pdf_output_path = 'financial_report.pdf'
        pdf.output(pdf_output_path, 'F')

         # Return the single PDF file
        return send_file(
            pdf_output_path,
            as_attachment=True,
            download_name=pdf_title + '.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        print(f'Failed to generate financial report: {str(e)}')
        return f'Failed to generate financial report: {str(e)}', 500




@app.route("/generateAPIKey", methods=["POST"])
@jwt_or_session_token_required
def generateAPIKey():
  try:
    user_email = extractUserEmailFromRequest(request)
  except InvalidTokenError:
    # If the JWT is invalid, return an error
    return jsonify({"error": "Invalid JWT"}), 401
  return GenerateAPIKeyHandler(request, user_email)


@app.route("/deleteAPIKey", methods=["POST"])
@jwt_or_session_token_required
def deleteAPIKey():
  verifyAuthForIDs(ProtectedDatabaseTable.API_KEYS, request.json["api_key_id"])
  return DeleteAPIKeyHandler(request)

@app.route('/getAPIKeys', methods = ['GET'])
@jwt_or_session_token_required
def getAPIKeys():
  try:
    user_email = extractUserEmailFromRequest(request)
  except InvalidTokenError:
    # If the JWT is invalid, return an error
    return jsonify({"error": "Invalid JWT"}), 401
  return GetAPIKeysHandler(request, user_email)


#For the SDK
#later will need to add @valid_api_key_required to all

USER_EMAIL_API = "api@example.com"

@app.route('/public/upload', methods = ['POST'])
@valid_api_key_required
def upload():
    print("Form data:", request.form)
    print("Files:", request.files)

    #chat_type = int(request.form.getlist('task_type')[0])  # Convert to int
    #model_type = int(request.form.getlist('model_type')[0])

    chat_type = request.form.getlist('task_type')[0]
    model_type = request.form.getlist('model_type')[0]

    user_email = USER_EMAIL_API

    print("CHAT TYPE IS", chat_type)
    if chat_type == "documents": #question-answering
        print("question answer")
        files = request.files.getlist('files[]')
        paths = request.form.getlist('html_paths')

        print("paths is", paths)

        print("chat is is", chat_type)
        print("files are", files)

        #create a new user with user_email api@example.com
        ensure_SDK_user_exists(user_email)

        #create new chat
        model_number = 0 if model_type == "gpt" else 1 if model_type == "claude" else None
        chat_number = 0 if chat_type == "documents" else 1 if chat_type == "edgar" else None
        chat_id = add_chat_to_db(user_email, chat_number, model_number)

        #Ingest pdf
        MAX_CHUNK_SIZE = 1000

        for file in files:
            print("file is here")
            result = p.from_buffer(file)
            text = result["content"].strip()

            filename = file.filename

            doc_id, doesExist = add_document_to_db(text, filename, chat_id=chat_id)

            if not doesExist:
                #chunk_document.remote(text, MAX_CHUNK_SIZE, doc_id)
                result_id = chunk_document.remote(text, MAX_CHUNK_SIZE, doc_id)
                result = ray.get(result_id)
        for path in paths:

            text = get_text_from_url(path)

            doc_id, doesExist = add_document_to_db(text, path, chat_id=chat_id)

            if not doesExist:
                #chunk_document.remote(text, MAX_CHUNK_SIZE, doc_id)
                result_id = chunk_document.remote(text, MAX_CHUNK_SIZE, doc_id)
                result = ray.get(result_id)
    elif chat_type == "edgar": #edgar
        print("ticker")
        ticker = request.form.getlist('ticker')[0]

        ensure_SDK_user_exists(user_email)

        #create new chat
        model_number = 0 if model_type == "gpt" else 1 if model_type == "claude" else None
        chat_number = 0 if chat_type == "documents" else 1 if chat_type == "edgar" else None
        chat_id = add_chat_to_db(user_email, chat_number, model_number)

        if ticker:
            MAX_CHUNK_SIZE = 1000

            reset_uploaded_docs(chat_id, user_email)


            url, ticker = download_10K_url_ticker(ticker)
            filename = download_filing_as_pdf(url, ticker)

            text = get_text_from_single_file(filename)

            print("test1")
            doc_id, doesExist = add_document_to_db(text, filename, chat_id)

            if not doesExist:
                #print("test")
                #chunk_document.remote(text, MAX_CHUNK_SIZE, doc_id)
                result_id = chunk_document.remote(text, MAX_CHUNK_SIZE, doc_id)
                result = ray.get(result_id)
    else:
        return jsonify({"id": "Please enter a valid task type"}), 400

    return jsonify({"id": chat_id}), 200


@app.route('/public/chat', methods=['POST'])
@valid_api_key_required
def public_ingest_pdf():
    user_email = USER_EMAIL_API
    ensure_SDK_user_exists(user_email) #do this here in case the user hasn't uploaded a document yet

    message = request.json['message']
    chat_id = request.json['chat_id']

    model_type, task_type = get_chat_info(chat_id)

    model_key = request.json['model_key']

    #at the moment don't think we need to add it to the db?
    #if model_key:
    #    add_model_key_to_db(model_key, chat_id, user_email)

    query = message.strip()

    #This adds user message to db
    add_message_to_db(query, chat_id, 1)

    #Get most relevant section from the document
    sources = get_relevant_chunks(2, query, chat_id, user_email)
    sources_str = " ".join([", ".join(str(elem) for elem in source) for source in sources])

    sources_swapped = [[str(elem) for elem in source[::-1]] for source in sources]
    print('sources swapped', sources_swapped)

    if (model_type == 0):
        if model_key:
           model_use = model_key
        else:
           model_use = "gpt-4o-mini"

        print("using OpenAI and model is", model_use)
        client = openai.OpenAI()
        try:
            completion = client.chat.completions.create(
                model=model_use,
                messages=[
                    {"role": "user",
                     "content": f"You are a factual chatbot that answers questions about uploaded documents. You only answer with answers you find in the text, no outside information. These are the sources from the text:{sources_str} And this is the question:{query}."}
                ]
            )
            print("using fine tuned model")
            answer = str(completion.choices[0].message.content)
        except openai.NotFoundError:
            print(f"The model `{model_use}` does not exist. Falling back to 'gpt-4'.")
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user",
                     "content": f"First, tell the user that their given model key does not exist, and that you have resorted to using GPT-4 before answering their question, then add a line break and answer their question. You are a factual chatbot that answers questions about uploaded documents. You only answer with answers you find in the text, no outside information. These are the sources from the text:{sources[0]}{sources[1]} And this is the question:{query}."}
                ]
            )
            answer = str(completion.choices[0].message.content)
    else:
        print("using Claude")

        if model_key:
           return jsonify({"Error": "You cannot enter a fine-tuned model key when using Claude"}), 400

        anthropic = Anthropic(
            api_key = os.getenv("ANTHROPIC_API_KEY")
        )

        completion = anthropic.completions.create(
            model="claude-2",
            max_tokens_to_sample=700,
            prompt = (
              f"{HUMAN_PROMPT} "
              f"You are a factual chatbot that answers questions about uploaded documents. You only answer with answers you find in the text, no outside information. "
              f"please address the question: {query}. "
              f"Consider the provided text as evidence: {sources_str}. "
              f"{AI_PROMPT}")
        )
        answer = completion.completion

    #This adds bot message
    message_id = add_message_to_db(answer, chat_id, 0)

    try:
        add_sources_to_db(message_id, sources)
    except:
        print("no sources")

    return jsonify(message_id=message_id, answer=answer, sources=sources_swapped) #can modify the sources here if we don't want to return the sources

@app.route('/public/evaluate', methods = ['POST'])
@valid_api_key_required
def evaluate():
    message_id = request.json['message_id']
    user_email = USER_EMAIL_API

    question_json, answer_json = get_message_info(message_id, user_email)

    question = question_json['message_text']
    answer = answer_json['message_text']
    context = answer_json['relevant_chunks']

    #get it in the corret data format to put in ragas
    if not isinstance(context, list):
        context = [context]

    contexts = [context]

    data = {
        "question": [question],
        "answer": [answer],
        "contexts": contexts
    }

    dataset = Dataset.from_dict(data)

    result = ragas.evaluate(
        dataset = dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
        ],
    )

    return result


if __name__ == '__main__':
    app.run(port=5000)
