readImg = (input, ouput) => {
    if(input.files && input.files[0]){
    var reader = new FileReader();
        reader.onload = (e) => {
        var src = e.target.result;
       $(ouput).html('<img src="'+src+'"/>');
       $(ouput).find('img').css({'width':'300px', 'height':'80px', 
       'border-radius':'8px', 'margin-top':'4px', 'margin-bottom':'4px'});
        };
        reader.readAsDataURL(input.files[0]);
    }
    }

readFilm = (input, output) => {
    if(input.files && input.files[0]){
        let file = input.target.files[0];
        let src = URL.createObjectURL(file);
        $(output).html('<video src="'+src+'" controls autoplay/>Browser of no support for video</video>');
        $(output).find('video').css({'width':'300px', 'height':'80px','border-radius':'8px', 'margin-top':'4px', 'margin-bottom':'4px'});
    alert(file + src + output + input );
    }
}

    document.getElementById("videoUpload").onchange = function(event) {
        let file = event.target.files[0];
        let blobURL = URL.createObjectURL(file);
        document.querySelector("video").style.display = 'block';
        document.querySelector("video").src = blobURL;
      }

      <input type='file'  id='videoUpload'/>
      <video width="320" height="240" style="display:none" controls autoplay>
        Your browser does not support the video tag.
      </video>