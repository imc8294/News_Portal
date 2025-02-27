$("#login-button").click(function(){
	let email = $("#email").val()
	let password = $("#password").val()
	error = false
	if(email == ''){
		error = true
		$(".email-error").text('Email id is required')
	}else{
		error = false
		$(".email-error").text('');
	}

	if(password == ''){
		error = true
		$(".password-error").text('Password is required')
	}else{
		error = false
		$(".password-error").text('');
	}

	if(error == false){
		$("#login-form").submit();
	}
});

$("#submitSearchButton").click(function(){
	let startDate = $("#start_date").val();
	let lastDate = $("#last_date").val();
	let keyword = $("#keyword").val();
	error = false
	if(startDate == ''){
		error = true
		$(".start_date_error").text('First Date is required')
	}else{
		error = false
		$(".start_date_error").text('');
	}

	if(lastDate == ''){
		error = true
		$(".end_date_error").text('Last Date is required')
	}else{
		error = false
		$(".end_date_error").text('');
	}

	if(keyword == ''){
		error = true
		$(".keyword_error").text('Keyword is required')
	}else{
		error = false
		$(".keyword_error").text('');
	}

	if(error == false){
		$("#search-form").submit();
	}
});


$(function () {
  $("#example1").DataTable({
    "responsive": true, "lengthChange": false, "autoWidth": true,
    "buttons": ["copy", "csv", "excel", "pdf", "print", "colvis"],
    "pageLength": 100,
    "aaSorting": []
  }).buttons().container().appendTo('#example1_wrapper .col-md-6:eq(0)');
});

function submit_changePassword(){
	let password = $("#password").val();
	let confirm_password = $("#confirm_password").val();
	if(password == ''){
		password_error = true
		$(".password_error").text('Password is required')
	}else{
		password_error = false
		$(".password_error").text('');
	}

	if(confirm_password == ''){
		con_error = true
		$(".confirm_password_error").text('Confirm Password is required')
	}else{
		con_error = false
		$(".confirm_password_error").text('');
	}

	if (password == confirm_password){
		confirm_password = true
		$(".confirm_password_err").text('');
	}else{
		confirm_password = false
		$(".confirm_password_err").text('Confirm Password is not same as password')
	}

	if(confirm_password == true && con_error == false && password_error == false){
		$("#change-password-form").submit()
	}


}