const numImagesPerLoad = 10;
const thumbnailsContainer = document.getElementById('thumbnails');
let startIndex = 0;
let impressedVideoIds = [];

function createThumbnail(item) {
   const thumbnailDiv = document.createElement('div');
   thumbnailDiv.classList.add('thumbnail');

   const img = document.createElement('img');
   img.src = item.video_thumbnail;
   img.alt = item.video_title;

   const title = document.createElement('p');
   title.innerHTML = item.video_title;

   thumbnailDiv.addEventListener('click', () => {
       window.location.href = `${itemDetailUrl}${item.video_id}`;
       document.cookie = `impressed_video_ids=${JSON.stringify(impressedVideoIds)}`;
   });

   thumbnailDiv.appendChild(img);
   thumbnailDiv.appendChild(title);

   return thumbnailDiv;
}

function loadThumbnails() {
   const endIndex = Math.min(startIndex + numImagesPerLoad, items.length);
   for (let i = startIndex; i < endIndex; i++) {
       thumbnailsContainer.appendChild(createThumbnail(items[i]));
       impressedVideoIds.push(items[i].video_id);
   }
   startIndex = endIndex;
}

function scrollHandler() {
   if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight) {
       loadThumbnails();
   }
}

window.addEventListener('load', () => {
   loadThumbnails();
   window.addEventListener('scroll', scrollHandler);
});