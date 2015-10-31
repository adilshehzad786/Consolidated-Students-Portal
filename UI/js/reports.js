$(document).ready(function(){
			$('.table_div').hide();
			$('#back_div').hide();
			$('#search_bar').hide();
			$('#run_query').click(function(){
				$('#Hide').slideUp();
				$('.table_div').show();
				$('#back_div').show();
			});
			$('#back_query').click(function(){
				$('#Hide').slideDown();
				$('.table_div').hide();
				$('#back_div').hide();
			});
			$('#search_click').click(function(){
				$('#search_bar').slideToggle();
			
			});
			$('.filters').hide();
			$('#semester_list').hide();
			$('#course_list').hide();
			$('#help').hide();
			$('#ListofQueries li').click(function(){
				alert("WEHOWFOWFJOE");
			});
			$('#querytype').change(function(){
				$('.filters').hide();
				var K = $('#querytype').val();
				$('.' + K).show();
			});
			$('#maintype').change(function(){
				$('#semester_list').hide();
				$('#course_list').hide();
				var K = $('#maintype').val();
				if( K == 'semester')
					$('#semester_list').show();
				if( K == 'courses')
					$('#course_list').show();
			});
			$('#add_query').click(function(){
				if( $('#maintype').val() == '-1')
					alert("Must Select One of Course, Career or Semester");
				else{
				var K = $('#querytype').val();
				var string = ""
				flag = 0
				if( K == 'batch')
				{
					string += "Batch"
					string += " "
					if($('#batchInput1').val() != "" & $('#batchInput2').val() != "" ) 
						string += $('#batchInput1').val() + " " + $('#batchInput2').val();
					else{
						flag = -1
					}
				} else if( K == 'programme')
				{
					string += "Programme"
					string += " "
					if($('#programmeInput1').val() != null & $('#programmeInput2').val() != null ) 
						string += $('#programmeInput1').val() + " " + $('#programmeInput2').val()
					else
						flag = -1
				}
				else if( K == 'sgpa')
				{
					string += "SGPA"
					string += " is "
					if($('#gpaInput3').val() != "" & $('#gpaInput4').val() != "" & $('#operationInput').val() != "" )
						string += $('#operationInput').val() + " " + $('#gpaInput3').val() + " and " + $('#gpaInput4').val() +" for "
					else{
						flag = -1
					}
					if($('#maintype').val() == 'semester')
						string += $('#semester_list').val()
					else{
						flag = -2
						alert('This filter requires the  \'Semester\' option');
					}
				}
				else if( K == 'cgpa')
				{
					string += "CGPA"
					string += " is "
					if($('#gpaInput3').val() != "" & $('#gpaInput4').val() != "" & $('#operationInput').val() != "" )
						string += $('#operationInput').val() + " " + $('#gpaInput3').val() + " - " + $('#gpaInput4').val()
					else
						flag = -1
				}
				else if( K == 'grades')
				{
					string += "Grade"
					string += " is "
					if($('#gradeInput3').val() != "" & $('#gradeInput4').val() != "" & $('#operationInput').val() != "" )
						string += $('#operationInput').val() + " " + $('#gradeInput3').val() + " - " + $('#gradeInput4').val()
					else{
						flag = -1
					}
				}
				else if( K == 'marks')
				{
					string += "Marks"
					string += " are "
					string += $('#operationInput').val()
					string += " "
					if($('#percentageInput1').val() != "" & $('#percentageInput2').val() != "" & $('#marksInput5').val() != "" )
						string += $('#percentageInput1').val() + " - " + $('#percentageInput2').val() +" in " + $('#marksInput5').val()
					else{
						flag = -1
					}
				}
				else if( K == 'attendance')
				{
					string += "Attendance"
					string += " is between "
					if($('#percentageInput1').val() != "" & $('#percentageInput2').val() != "")
						string += $('#percentageInput1').val() + "% to " + $('#percentageInput2').val() + "%"
					else
						flag = -1
				}
				else if( K == 'timeperiod')
				{
					string += "Between"
					string += " "
					// alert($('#timeperiodInput3').val() + " and " + $('#timeperiodInput4').val())
					if($('#timeperiodInput3').val() != "" & $('#timeperiodInput3').val() != "" ) 
						string += $('#timeperiodInput3').val() + " and " + $('#timeperiodInput4').val();
					else
					{
						flag = -1
						
					}

				}
				if( flag == 0)
				{	$('.inline-list').append("<li><span class=\"del\">"+ string + "</span></li>");
					$('#help').show();
				}
				if(flag == -1)
				{
					alert('Required Fields are empty')
				}
				$('.filters').hide();
				
			}
			});
		});