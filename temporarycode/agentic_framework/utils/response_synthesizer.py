# utils/response_synthesizer.py
def synthesize_response(results):
    """
    Combine results from different agents into a final response.
    :param results: Dictionary of agent results.
    :return: Synthesized response string.
    """
    response_parts = []
    for agent, result in results.items():
        response_parts.append(f"{agent}: {result}")
    return "\n".join(response_parts)
