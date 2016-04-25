//global variable for the step being shown
var step = 0;

var mGRE_Q, mGRE_V, mGRE_W, mTOEFL, mUNI_RANK, mGPA, mMAJOR, mUNI_IMP, mCOST_IMP;

console.log("#dc"+step)
//on page load, show intro screen
$(document).ready(function(){
	updateDynamicContent();
});
//on next button click
$(document).ready(function(){
	$("#nextbutton").click(function(){
		if(isStepComplete(step)&&step<6)
		{
			step++;
			updateDynamicContent();
		}
	});
});
//on back button click
$(document).ready(function(){
	$("#backbutton").click(function(){
		if(step>0)
		{
			step--;
			updateDynamicContent();
		}
	});
});
//updates dynamic content
function updateDynamicContent()
{
	console.log("firing updateDynamicContent() with step "+step)
	$(".dc").css("visibility","hidden");
	$("#dc"+step).css("visibility","visible");
	$(".navLevel1").removeClass("nav1Highlighted");
	var splashText;
	switch(step)
	{
		case 0:
		splashText = 'Welcome to U11';
		$("#navGroup1").addClass("nav1Highlighted");
		break;
		case 1:
		splashText = 'Tell us more about your tests';
		$("#navGroup2").addClass("nav1Highlighted");
		break;
		case 2:
		splashText = 'Where did you do your undergraduate studies?';
		$("#navGroup2").addClass("nav1Highlighted");
		break;
		case 3:
		splashText = 'Which major are you aiming for?';
		$("#navGroup3").addClass("nav1Highlighted");
		break;
		case 4:
		splashText = 'How important is college ranking to you?';
		$("#navGroup3").addClass("nav1Highlighted");
		break;
		case 5:
		splashText = 'How important is cost of attendence to you?';
		$("#navGroup3").addClass("nav1Highlighted");
		break;
		case 6:
		splashText = 'Here are the best colleges for you!';
		$("#navGroup4").addClass("nav1Highlighted");
		executeClassifier();
		break;
	}
	$("#splash-text").html(splashText);
	//TODO: if step == 6, process results
}

function isStepComplete()
{
	//FOR DEBUG
	return true;

	switch(step)
	{
		case 0:
		return true;
		case 1:
		mGRE_Q = parseInt(document.getElementById("GRE-Q").value); console.log("mGRE_Q is "+mGRE_Q);
		mGRE_V = parseInt(document.getElementById("GRE-V").value); console.log("mGRE_V is "+mGRE_V);
		mGRE_W = parseInt(document.getElementById("GRE-W").value); console.log("mGRE_W is "+mGRE_W);
		mTOEFL = parseInt(document.getElementById("TOEFL").value); console.log("mTOEFL is "+mTOEFL);
		if(isNaN(mGRE_Q)||isNaN(mGRE_V)||isNaN(mGRE_W)||isNaN(mTOEFL))
			return false;
		break;
		case 2:
		mUNI_RANK = parseInt(document.getElementById("UNI-RANK").value);
		mGPA = parseInt(document.getElementById("GPA").value);
		if(isNaN(mUNI_RANK)||isNaN(mGPA))
			return false;
		break;
		default:
		return true;
	}
	return true;
}

function executeClassifier() {
	    data = {'gre_q' : '4',
				'gre_v' : '4',
				'gre_w' : '4',
				'toefl' : '4',
				'uni_rank' : '4',
				'gpa' : '4',
				'major' : 'cs',
				'uni_imp' : '0',
				'cost_imp' : '0'}
		console.log(JSON.stringify(data, null, '\t'));

	$.ajax({
		type: "POST",
		url: "http://localhost:5000/api/classify",
		contentType: 'application/json;charset=UTF-8',
		data: JSON.stringify(data, null, '\t'),
		success: function(response) {
			console.log(response);
		}
	});
}