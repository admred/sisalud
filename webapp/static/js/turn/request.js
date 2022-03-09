var $form=$('#form-1') || $('form') ;

$(document).ready(function(){
    ajax_select('/ajax/speciality','speciality','Especialidad');
});

$(document).on('change','#speciality-1',function(){
    $('#g-doctor-1').remove();
    $('#g-turn-1').remove();
    $('#g-submit-1').remove();
    ajax_select('/ajax/doctor_by_speciality/'+this.value,'doctor',"Medico");
});

$(document).on('change','#doctor-1',function(){
    $('#g-turn-1').remove();
    $('#g-submit-1').remove();
    ajax_table('/ajax/turn_by_doctor/'+this.value,'turn','Turnos Libres');
});

$(document).on('change','input[type="radio"]:checked',function(){
    if( $('#g-submit-1').length == 0){
        $form.append('<button type="submit" id="g-submit-1" class="btn btn-success float-right">Aceptar</button>');
    }
});


var old_datetime;
var old_duration;
$('#when').on('change',function(){
    if(old_datetime){
        if(old_datetime + $('#duration-1').val != this.value){
            console.log('return');
            return;
        }
    }
    old_duration=$('#duration-1').val;
    old_datetime=this.value;
    console.log('old_datetime     = '+old_datetime);
    console.log('current_datetime = '+this.value);
});

$('#patient-dni-1').on('focusout',function(){
    const _url='/ajax/patient_by_dni/'+this.value;
    $.get({
        url:_url,
        async:false
    }).done(function(response){
        const data=response.data;
        console.log('data = '+data);

        $('#patient-msg-1').empty();
        $('#patient-id-1').val("");
        if(data  == undefined || data == ''){
            console.log('data = '+data);
            $('#patient-msg-1').html('DNI no econtrado');
        }else{
            $('#patient-msg-1').html(data['fullname']);
            $('#patient-id-1').val(data['id']);
        }
    });
});

function ajax_select(url,name,title){
    $.get({
        url:url,
        async:false
    }).done(function(response){
        var opts='<option value="-1" disabled hidden selected></option>';
        var data=response.data;
        for(i=0;i<data.length;i++){
            opts+='<option value="'+data[i][0]+'">'+data[i][1]+'</option>';
        }
        $form.append('<div class="form-group mt-5" id="g-'+name+'-1"><label>'+title+'</label><select class="form-control" id="'+name+'-1" name="'+name+'">'+opts+'</select></div>');
    });
};

function ajax_table(url,name,title){
    $.get({
        url:url,
        async:false
    }).done(function(response){
        var opts='';
        var data=response.data;
        for(i=0;i<data.length;i++){
            opts+='<tr><td><input type="radio" name="'+name+'" value="'+data[i][0]+'"/></td><td>'+data[i][1]+'</td></tr>';
        }
        $form.append('<div class="form-group mt-5" id="g-'+name+'-1"><label>'+title+'</label><table class="table"><tbody>'+opts+'</tbody></table></div>');
    });
};
