var user = {
    create_username_from_email: function(email){
        username =  String(email).split('@')[0];
        return username;
    },
    validate_email: function(email, form_field){
        
        form_field.parent().parent().removeClass('has-error').removeClass('has-success');
        if( email.indexOf('@') < 1){
            return false;
        }
        
        $('[type=submit]').prop('disabled', true);
        
        $.ajax({
            url: '/users/validate_email',
            data: {email: email}
        }).done(function(response){ 
             form_field.parent().parent().removeClass('has-error').addClass('has-success');
             username = user.create_username_from_email(response.result);
             $('[name=username]').val(username);
             $.ajax({
                 url: '/users/generate_password',
                 data: {username: username}
             }).done(function(response){
                 $('[name=password]').val(response.result);
                 $('[type=submit]').prop('disabled', false);
             });
            
        }).fail(function(xhr){
            $('[name=username]').val('');
            $('[name=password]').val('');
            $('[type=submit]').prop('disabled', true);
            form_field.parent().parent().addClass('has-error');
            toastr.error('Email address already exists. Would you like to edit this username instead?\
&nbsp;&nbsp;<button class="btn btn-sm btn-danger yes_edit">Yes</button>');
            
        });
    },
    
    submit_create_form: function(){
         $('[name=create_user]').submit(function(e){
              e.preventDefault();
              $('.loading').hide().show();
              toastr.info('Creating User..');
             
              $.ajax({
                   url: '/users/manage',
                   type: 'POST',
                   data:  $('[name=create_user]').serialize()
              }).done(function(response){
                   $('.create_user_top_content').html('<div class="alert alert-success" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+response.success+'</div>');
              }).fail(function(xhr){
                  $('.create_user_top_content').html(user.errorTemplate(xhr.responseJSON));
                  
              }).always(function(){
                  $('.loading').hide();
              });
         });
    },
    
    errorTemplate: function($context){
        msgs = '<div class="alert alert-danger" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
        
        $.each($context, function(i, message){
             $.each(message, function(k, msg){
                 msgs += '<strong>'+msg+'</strong>';
                 msgs += '<ul>';
                 $.each(message[msg], function(l, m){ 
                    msgs += '<li>'+m+'</li>'
                 });
                 msgs += '</ul>';
             });
        });
       msgs += '</div>';
       return msgs
    },
    deleteUser: function(){
         $('[name=delete_btn]').click(function(e){
               $('.loading').hide().show();
               toastr.info('Deleting User..');
               $.ajax({
                   url: '/users/delete',
                   type: 'POST',
                   data:  $('[name=create_user]').serialize()
                  }).done(function(response){
                       $('.create_user_top_content').html('<div class="alert alert-success" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+response.success+'</div>');
                       $('[name=create_user]').trigger('reset');
                       $('[name=search_form]').trigger('reset');
                    
                  }).fail(function(xhr){
                      $('.create_user_top_content').html('<div class="alert alert-success" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+xhr.responseJSON.error+'</div>');
                  }).always(function(){
                      $('.loading').hide();
               });
             
         });
    }
};