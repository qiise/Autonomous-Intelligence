// import React from "react";

// function LPHighLevel({ image, title, description }) {
//   return (
//     <div class="bg-black py-10 rounded mb-4 overflow-hidden shadow-lg transition-all duration-500">
//       <img
//         class={`w-full ${title == "Define Your Target" ? " h-16" : "h-20"}`}
//         src={image}
//         alt={title}
//         loading="lazy"
//       />
//       <div class="px-6 py-4 ">
//         <div class="font-bold text-xl mb-2 text-center py-4 text-[#40C6FF]">{title}</div>
//         <p class="text-gray-300 text-base text-center">{description}</p>
//       </div>
//     </div>
//   );
// }

// export default LPHighLevel;

import React from "react";

function LPHighLevel({ image, title, description }) {
  return (
    <div class="bg-gray-950 py-10 rounded mb-4 overflow-hidden shadow-lg transition-all duration-500">
      {/* Flex container to center the image */}
      <div class="flex justify-center">
        <img
          class={`${title == "Define Your Target" ? "h-16" : "h-20"} w-auto`} // Adjusted class to not be full width and to apply conditional height
          src={image}
          alt={title}
          loading="lazy"
        />
      </div>
      <div class="px-6 py-4 ">
        <div class="font-bold text-xl mb-2 text-center py-4 text-[#40C6FF]">{title}</div>
        <p class="text-gray-300 text-base text-center">{description}</p>
      </div>
    </div>
  );
}

export default LPHighLevel;
