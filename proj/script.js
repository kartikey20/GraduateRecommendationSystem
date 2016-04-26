var debug = false;

//global variable for the step being shown
var step = 0;

var mGRE_Q, mGRE_V, mGRE_W, mTOEFL, mUNI_RANK, mGPA, mMAJOR, mUNI_IMP, mCOST_IMP;

var majors = {'Aerospace' : 'AE', 
			  'Biomedical' : 'BME',
			  'Biostatistics' : 'BIOSTAT',
			  'Chemical' : 'Chem',
			  'Civil' : 'CE',
			  'Computer Science' : 'CS',
			  'Geology / Earth Science' : 'GEO',
			  'Electrical and Computer Engineering' : 'ECE',
			  'Economics' : 'Econ',
			  'Education' : 'Edu',
			  'Electrical Engineering' : 'EE',
			  'Environmental Engineering' : 'ENENG',
			  'Financial' : 'Business',
			  'Industrial / Operations Research' : 'ISI',
			  'Material' : 'Material',
			  'Math' : 'Math',
			  'Mechanical' : 'Mech',
			  'Information Science / Data Science' : 'Data',
			  'Physics' : 'Physics'
			 };
var showAlert = true;


console.log("#dc"+step)
//on page load, show intro screen
$(document).ready(function(){

	dropdown_options = "";
	$.each(majors, function(i, row) {
		dropdown_options = dropdown_options + "<option>" + i + "</option>";
	});

	$("#MAJOR").html(dropdown_options);
	updateDynamicContent();
});
//on next button click
$(document).ready(function(){
	$("#nextbutton").click(function(){
		if(!debug && !isStepComplete(step)) {
			if(showAlert) {
				alert("Please Fill all fields correctly before continuing to the next page.");
				showAlert = false;
			}
		} else if(step<6) {
			step++;
			updateDynamicContent();
			showAlert = true;
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

	highlight_unfilled = function(box, validater) {
		if (!box[0].value || !validater(box[0].value)){
			$(box).css("border-color", 'red');
				return false;
		} else {
			$(box).css("border-color", "black");
			return true;
		}
	}

	validate_gre_vq = function(value) {
		var val = parseInt(value);
		if((val >= 130 && val <= 170) || (val >= 200 && val <= 800)) {
			return true;
		} else {
			return false;
		}
	}

	validate_gre_w = function(value) {
		var val = parseFloat(value);
		return (value >= 0 && value <= 6);
	}

	validate_toefl = function(value) {
		var val = parseInt(value);
		return (value >= 0 && value <= 120);
	}

	validate_gpa = function(value) {
		var val = parseFloat(value);
		return (value >= 0 && value <= 4.0);
	}

	validate_unirank = function(value) {
		var val = parseInt(value);
		return (val >= 1 && value <= 1000);
	}

	switch(step)
	{
		case 0:
		return true;
		case 1:
			var allSet = highlight_unfilled($("#GRE-Q"), validate_gre_vq) &
			highlight_unfilled($("#GRE-V"), validate_gre_vq) &
			highlight_unfilled($("#GRE-W"), validate_gre_w) &
			highlight_unfilled($("#TOEFL"), validate_toefl);

			if(allSet) {
				mGRE_Q = parseInt($("#GRE-Q")[0].value);
				mGRE_V = parseInt($("#GRE-V")[0].value);
				mGRE_W = parseInt($("#GRE-W")[0].value);
				mTOEFL = parseInt($("#TOEFL")[0].value);
			}

			return allSet;

		break;
		case 2:
			var allSet = highlight_unfilled($("#UNI-RANK"), validate_unirank) &
						 highlight_unfilled($("#GPA"), validate_gpa);

			if(allSet) {
				mUNI_RANK = parseInt($("#UNI-RANK")[0].value);
				mGPA = parseFloat($("#GPA")[0].value);
			}

			return allSet;
		break;
		case 3:
			mMAJOR = majors[$("#MAJOR")[0].value];
		break;
		case 4:
			mUNI_IMP = parseFloat($("#RANK-IMPORTANCE")[0].value)/100.0;
		break;
		case 5:
			mCOST_IMP = parseFloat($("#COST-IMPORTANCE")[0].value)/100.0;
		break;
		default:
		return true;
	}
	return true;
}

function updateResults(results) {
	var thead = "<thead><tr>" + "<td>University</td>" + 
				"<td align='center'>Ranking</td>" + "<td align='center'>Cost of Attendence</td>" +
				"<td align='right'>Chance</td>" + "</tr></thead>";
	
	var tbody = "<tbody>";

	$.each(results, function(i, row) {
		tbody = tbody + "<tr>";
		univ = "<a href=http://" + row['url'] + ">" + row['university'] + "</a>";
		cost = "$" + parseFloat(row['cost']);
		ranking = "#" + parseInt(row['ranking']);
		chance = parseFloat(row['chance'] * 100).toFixed(2) + "%";

		tbody = tbody + "<td>" + univ + "</td>" +
						"<td align='center'>" + ranking + "</td>" +
						"<td align='center'>" + cost + "</td>" +
						 "<td align='right'>" + chance + "</td>"

				+ "</tr>";
	});

	tbody = tbody + "</tbody";

	var html_table = "<table class='res_table' align='center'>" + thead + tbody + "</table>";
	console.log(html_table);
	$("#dc6").html(html_table);
}

function executeClassifier() {

		console.log(mGRE_Q, mGRE_V, mGRE_W, mTOEFL, mUNI_RANK, mGPA, mMAJOR, mUNI_IMP, mCOST_IMP);


	    data = {'gre_q' : 4,
				'gre_v' : 4,
				'gre_w' : 4,
				'toefl' : 4,
				'uni_rank' : 4,
				'gpa' : 4,
				'major' : '4',
				'uni_imp' : 0.5,
				'cost_imp' : 0.5}
		//console.log(JSON.stringify(data, null, '\t'));

	$.ajax({
		type: "POST",
		url: "http://localhost:5000/api/classify",
		contentType: 'application/json;charset=UTF-8',
		data: JSON.stringify(data, null, '\t'),
		success: function(response) {
			updateResults(response['results']);
		}
	});
}