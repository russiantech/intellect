
$(document).ready( () => {

    const loadBtn = document.getElementById('loadbtn');
    const loadBtnB4 = $(loadBtn).html();
    const total = document.getElementById('total').textContent;
    const view_all  = document.getElementById('view_all');

    $(loadBtn).click( () =>{ loadMore() });
    $(view_all).click( () =>{ loadMore() });

    loadMore = () => {

        const content_container = $("#content_container");
        var content_count = content_container.children().length;
        
        //alert(content_container.children().length)
        //console.log(content_count);

        //if (content_count < total ) { content_count = total; loadMore(); console.log(content_count); return  }
        $(view_all).click( () => { (content_count < total ) ? content_count = total : ''; console.log(content_count); });
        
       // $(view_all).click( () => {
        //    if (content_count < total ) { content_count = total;  loadMore(); console.log(content_count); alert(content_count); }
           // var content_count = total;  console.log(content_count);  
       // });


        $.ajax({

          url: '{{url_for("x_course_api.loadmore")}}',
          type: 'GET',
          data: { 'offset': content_count },

          beforeSend: () => { 
                //alert(content_count);
            $(loadBtn).html('<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span> loading...')
          },

          success:  (response) => {
            
              $(loadBtn).html(loadBtnB4);
            
              //location.reload();
            //console.log(content_count);
            //content_count = $('.content_').reload;
           // content_count += Object.keys(response).length
            //alert(content_count);

            //alert(content_count >= total );
                        
            if (content_count >= total ) {
            //alert('e don do')
            $(loadBtn).html('<span class="danger" aria-hidden="true"> 0 . Contents </span>');
            $(loadBtn).addClass('isDisabled');
             return }else{
            $(loadBtn).html(loadBtnB4);
            $(loadBtn).removeClass('isDisabled');
            }

              response?.map( data => {

                  $(content_container).append(

                  `
                  <div class="col">
                        <div class="card h-100">
                            <img src="/static/img/course/${data.photo}" class="card-img-top sh-22" alt="card image">
                            <div class="card-body">
                                <h5 class="heading mb-0">
                                    <a href="/course/${data.slug}" class="body-link stretched-link">${data.title}</a>
                                </h5>
                            </div>
                            <div class="card-footer border-0 pt-0">
                                <div class="mb-2">
                                    <div class="br-wrapper br-theme-cs-icon d-inline-block">
                                        <div class="br-wrapper">
                                            <select class="rating" name="rating" autocomplete="off" data-readonly="true" data-initial-rating="5" style="display: none;">
                                                <option value="1">1</option>
                                                <option value="2">2</option>
                                                <option value="3">3</option>
                                                <option value="4">4</option>
                                                <option value="5">5</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="text-muted d-inline-block text-small align-text-top">(0)</div>
                                </div>
                                <div class="card-text mb-0">
                                    <div class="text-muted text-overline text-small">
                                        <del>$ ${data.id} </del>
                                    </div>
                                    <div>$ ${data.fee}</div>
                                </div>
                            </div>
                            {% if current_user.is_authenticated and current_user.is_admin() %}
                            <a href="/editor/${data.id}" 
                            class="position-relative stretched-link d-inline-block mt-3" data-bs-toggle="tooltip" data-bs-placement="top" title="" 
                            data-delay="{'show':'100', 'hide':'0'}" data-bs-original-title="edit ${data.title}"> 
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="acorn-icons acorn-icons-edit icon"><path d="M14.6264 2.54528C15.0872 2.08442 15.6782 1.79143 16.2693 1.73077C16.8604 1.67011 17.4032 1.84674 17.7783 2.22181C18.1533 2.59689 18.33 3.13967 18.2693 3.73077C18.2087 4.32186 17.9157 4.91284 17.4548 5.3737L6.53226 16.2962L2.22192 17.7782L3.70384 13.4678L14.6264 2.54528Z"></path></svg>
                            </a>
                            {% endif %}
                        
                        </div>
                    </div>

                  `)

              });

    },

    error: (err) => { console.log(err); },
      
});

}



  
  });
