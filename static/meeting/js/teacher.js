// For CDN version default
ZoomMtg.setZoomJSLib('https://source.zoom.us/1.8.5/lib', '/av'); 
ZoomMtg.preLoadWasm();
ZoomMtg.prepareJssdk();
const zoomMeeting = document.getElementById("zmmtg-root")

const meetConfig = {
	apiKey: 'tgs2Q91LTDqTwMZneinf0w',
	meetingNumber:mid,
	leaveUrl: '/faculty/',
	userName: username,
	userEmail: email,
	passWord: pass, 
	role: 1, // 1 for teacher 0 for student
	lang:'en-US',
 
  webEndpoint:'/faculty/',
};
getSignature(meetConfig);
function getSignature(meetConfig) {
	fetch(`http://127.0.0.1/faculty/meetingdata`, {
			method: 'POST',
			body: JSON.stringify({ meetingData: meetConfig })
		})
		.then(result => result.text())
		.then(response => {
			ZoomMtg.init({
				leaveUrl: meetConfig.leaveUrl,
				isSupportAV: true,
				success: function() {
					ZoomMtg.join({
						signature: response,
						apiKey: meetConfig.apiKey,
						meetingNumber: meetConfig.meetingNumber,
						userName: meetConfig.userName,
						// password optional; set by Host
						passWord: meetConfig.passWord,
						success: function(res) {

							ZoomMtg.showRecordFunction({
								show: true
							 });
						},
				
						error(res) { 
							console.log(res) 
						}
					})		
				}
			});
		
			ZoomMtg.showRecordFunction({
				show: true
			 });
			ZoomMtg.inMeetingServiceListener('onUserJoin', function (data) {
				console.log('inMeetingServiceListener onUserJoin', data);
			  });
			
			  ZoomMtg.inMeetingServiceListener('onUserLeave', function (data) {
				console.log('inMeetingServiceListener onUserLeave', data);
			  });
			
			  ZoomMtg.inMeetingServiceListener('onUserIsInWaitingRoom', function (data) {
				console.log('inMeetingServiceListener onUserIsInWaitingRoom', data);
			  });
			
			  ZoomMtg.inMeetingServiceListener('onMeetingStatus', function (data) {
				console.log('inMeetingServiceListener onMeetingStatus', data);
			  });
	});
}
