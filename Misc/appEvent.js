 function callAndroid(e,url,videoId){
	// 由于对象映射，所以调用test对象等于调用Android映射的对象
	if(mjs)
		mjs.invokeVideo(JSON.stringify({videoUrl:url,videoId:videoId}));
	e.stopPropagation();
 }
		 