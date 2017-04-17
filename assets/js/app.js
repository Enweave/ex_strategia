"use strict";

var $doc = $(document);

var runComments = function($form){
    var $body = $("html, body");
    var $last_touched_comment = undefined;
    var $form_initial_container = $('.js-comments-form-origin');
    var $root = $('.comments-root');

    $form.$comment_id = $form.find('[name="parent_comment"]');
    $form.$cancel_button = $form.find('.js-comments-form-cancel');
    $form.is_free = true;

    var bindComments = function($comments) {
        $comments.each(function(i) {
            var $comment = $comments.eq(i);
            $comment.comment_id = $comment.data('comment-id');
            $comment.$insert = $comment.find('.js-comments-insert-container--' + $comment.comment_id);
            $comment.$control_container = $comment.find('.js-comments-control-container--' + $comment.comment_id);
            $comment.$more = $comment.find('.js-comments-more--' + $comment.comment_id);
            $comment.$children_container = $comment.find('.js-comments-children-container--' + $comment.comment_id);

            $comment.find('.js-comments-reply--' + $comment.comment_id).on('click', function(e) {
                e.preventDefault();
                if ($last_touched_comment !== $comment) {
                    $comment.$control_container.toggleClass('active', true);
                    $comment.$insert.append($form);
                    $form.toggleClass('active', true);
                    $last_touched_comment = $comment;
                    $form.$comment_id.val($comment.comment_id);
                    $body.animate({scrollTop: $comment.offset().top - 30}, 200);
                }
            });

            $comment.is_free = true;
            $comment.$more.on('click', function() {
                if ($comment.is_free) {
                    $comment.is_free = false;
                    $.ajax({
                        type: 'GET',
                        data: {comment_id: $comment.comment_id },
                        url: $comment.$more.data('get-more-url'),
                        success: function(data) {
                            validator.showErrors(data["form_errors"]);
                            if (data['htmlData']) {
                                var $new = $(data['htmlData']);
                                bindComments($new);
                                $comment.$children_container.append($new);
                                $comment.$more.remove();
                            }

                            $comment.is_free = true;
                        },
                        error: function(textStatus) {
                            $comment.is_free = true;
                            try { console.log(textStatus) } catch(e) {}
                        }
                    });
                }
            });

        });
    };

    var cancelForm = function() {
        if ($last_touched_comment) {
            $last_touched_comment.$control_container.toggleClass('active', false);
            $form.toggleClass('active', false);
            $form_initial_container.append($form);
            $form.$comment_id.val('');
        }

        $last_touched_comment = undefined;
    };

    bindComments($('.js-comments-element'));

    $doc.keyup(function(e) {
        if (e.keyCode == 27) {
            cancelForm();
        }
    });

    $form.$cancel_button.on('click', function(e) {
        e.preventDefault();
        cancelForm();
    });

    $form.form = $form.find('form');

    $form.form.on('submit', function(e) {
        e.preventDefault();
    });

    var renderNewComment = function(commentHtml) {
        var $new = $(commentHtml);
        bindComments($new);
        if ($last_touched_comment) {
            $last_touched_comment.$children_container.append($new);
        } else {
            $root.append($new);
        }
    };

    var formSubmit = function() {
        if ($form.is_free === true) {
            var formData = $form.form.serialize();

            $form.is_free = false;
            return $.ajax({
                type: 'POST',
                data: formData,
                url: $form.form.attr("action"),
                success: function(data) {
                    validator.showErrors(data["form_errors"]);
                    if (data['success']) {
                        renderNewComment(data['commentHtml']);
                        alert(data['success']);
                        $form.form.trigger("reset");
                    }

                    $form.is_free = true;
                },
                error: function(textStatus) {
                    $form.is_free = true;
                    try { console.log(textStatus) } catch(e) {}
                }
            });
        }
    };

    var validator =  $form.form.validate({
        ignore: [],
        focusInvalid: false,
        // errorClass: 'has-error',
        errorPlacement:  function(error, element) {
            element.parent().toggleClass("has-error", true);
        },
        success: function(label, element) {
            $(element).parent().toggleClass("has-error", false);
        },

        invalidHandler: function(event, validator) {
            if (!validator.numberOfInvalids()) {
                return;
            }
        },

        submitHandler: function () {
            formSubmit();
        }
    });
};


$doc.ready(function(){
    var $form = $('.js-comments-form');
    if ($form.length) {
        runComments($form);
    }
});