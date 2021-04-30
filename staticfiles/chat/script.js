// variable list start

const months = ["JAN", "FEB", "MAR","APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
let current_datetime = new Date();
var datetimes = months[current_datetime.getMonth()] + " " + current_datetime.getDate() + " " + current_datetime.getFullYear() +" "+  current_datetime.getHours() + ":" + current_datetime.getMinutes() + ":" + current_datetime.getSeconds() ;
// variable list end
var recevierpic='';
var recevierid=0;
var newmsg='';
var senderfield='';

// alert(teacherid)

$(document).ready(function(){
 
    $('.msger-inputarea').ajaxForm(function(data) { 
        var sendermsg= $('#msgfield').val();
        senderfield=`
        <div class="msg right-msg">
        <div
        class="msg-img"
        style="background-image: url('/upload/${senderimg}')"
        ></div>

        <div class="msg-bubble">
            <div class="msg-info">
                <div class="msg-info-name">${sendername}</div>
                <div class="msg-info-time">${datetimes}</div>
            </div>

            <div class="msg-text">
                ${sendermsg}
            </div>
        </div>
    </div>
        `;
        $('#msgfield').val('');
        $('.msger-chat').append(senderfield);
        
        $('.msger-chat').scrollTop(12500);
        // $('.msger-chat').scrollTop += 500;
    }); 
    alluser();
});
// sidebar user start
function alluser(){
    var sidebardata='';

   
  
    $.ajax({
        url:'users',
        type:'GET',
        success:function(data){
            udata = eval(data);
            if(userrole=='Student'){
           
           for(x=0;x<udata.length; x++){
               sidebardata+=`
               <li class="contact ">
               <a href="javscript:void(0)" class="my-active" onclick="recevier(${udata[x].tid},'${udata[x].img}')">
                   <div class="wrap">
                       
                       <img class="img-fluid" src="${udata[x].img}" alt="s1.jpg" style="height:60px;">
                       <div class="meta">
                           <h5 class="name">${udata[x].First_Name} ${udata[x].Last_Name} </h5>
                           <br>
                       </div>
                   </div>
               </a>
           </li>
               `;

           }
          
        }
        
        else if(userrole=='Teacher'){
            for(x=0;x<udata.length; x++){
                sidebardata+=`
                <li class="contact">
                <a href="javascript:void(0)"  onclick="recevier(${udata[x].StudentId},'${udata[x].Profile}')">
                    <div class="wrap">
                        
                        <img class="img-fluid" src="${udata[x].Profile}"  alt="s1.jpg" style="height:60px;">
                        <div class="meta">
                            <h5 class="name">${udata[x].First_name} ${udata[x].Last_name} </h5>
                            <br>
                        </div>
                    </div>
                </a>
            </li>
                `;
            }
        }
        $('.alluser').html(sidebardata)
      
    }
    });   
}


// sidebar user end

// recevier
function recevier(x,y){
    recevierid=x;
    recevierpic=y;
    $('#rid').val(x);
    var element='';
    
    // old messages start
    $.ajax({
        url:'oldmessages',
        type:'GET',
        data:{
            'sender':senderid,
            'recevier':recevierid,
        },
        success: function(data){
            var msg = eval(data)
					    
            for(n=0; n<msg.length; n++){
                if(msg[n].msgfrom==senderid && msg[n].msgto==x ){
                 element +=`
                 
                 <div class="msg right-msg">
                 <div
                 class="msg-img"
                 style="background-image: url('/upload/${senderimg}')"
                 ></div>
         
                 <div class="msg-bubble">
                     <div class="msg-info">
                         <div class="msg-info-name">${msg[n].sender_name}</div>
                         <div class="msg-info-time">${msg[n].created_at}</div>
                     </div>
         
                     <div class="msg-text">
                         ${msg[n].msg}
                     </div>
                 </div>
             </div>
                
                 
                 `;
                }
                else if(msg[n].msgfrom==x && msg[n].msgto==senderid){
                element+=`	
                <div class="msg left-msg">
          <div
          class="msg-img"
          style="background-image: url('${recevierpic}')"
          ></div>

          <div class="msg-bubble">
              <div class="msg-info">
                  <div class="msg-info-name">${msg[n].sender_name}</div>
                  <div class="msg-info-time">${msg[n].created_at}</div>
              </div>

              <div class="msg-text">
                 ${msg[n].msg}
              </div>
          </div>
      </div>`;

                
                }
                // if condation end
                                
            }
            // for loop end
              $('.msger-chat').html(element);
              $('.msger-chat').scrollTop(12500);
        }
    }) 
    // old messages end

}



// pusher app setting
var channel = pusher.subscribe('chat'); // recevier
	  channel.bind('my-event', function(data) {
         
		  var msg = data['message'];
		   if(recevierid==data['sender'] && senderid==data['recevier']){
		  newmsg +=`
          <div class="msg left-msg">
          <div
          class="msg-img"
          style="background-image: url('${recevierpic}')"
          ></div>

          <div class="msg-bubble">
              <div class="msg-info">
                  <div class="msg-info-name">${data.sendername}</div>
                  <div class="msg-info-time">${data.datetime}</div>
              </div>

              <div class="msg-text">
                 ${msg}
              </div>
          </div>
      </div>

		  `
          $('.msger-chat').append(newmsg);
          $('.msger-chat').scrollTop(12500);
         
        }
       
	  });
	  Pusher.logToConsole = true;
	