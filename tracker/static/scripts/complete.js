$(document).ready(function() {
	$('.check-link').on("click", function() {
		var fullId = this.id;
		var id = fullId.split("-")[1];
		markComplete(id);
	});
});

function markComplete(id) {
	showWaitingIcon(id);
	$.ajax({
		url: "/markcomplete/" + id + "/",
		success: function(data) {
			resetCheckIcon(id);
			if (data=="Added") {
				showCompleted(id);
			}
			else if (data=="Deleted") {
				showIncompleted(id);
			}
			else {
				console.error("There was an error saving:");
				console.error(data);
			}
		},
		error: function(data) {
			console.log("There was an error: ");
			console.log(data);
			resetCheckIcon(id);
		}
	});
}

function showWaitingIcon(id) {
	$('#check-' + id + " i").removeClass("fa-check");
	$('#check-' + id + " i").addClass("fa-refresh");
	$('#check-' + id + " i").addClass("fa-spin");
}

function showCompleted(id) {
	$('#check-' + id + " > div").removeClass('unchecked');
	$('#check-' + id + " > div").addClass('checked');
}

function showIncompleted(id) {
	$('#check-' + id + ' > div').removeClass('checked');
	$('#check-' + id + ' > div').addClass('unchecked');
}

function resetCheckIcon(id) {
	$('#check-' + id + " i").addClass("fa-check");
	$('#check-' + id + " i").removeClass("fa-refresh");
	$('#check-' + id + " i").removeClass("fa-spin");
}
