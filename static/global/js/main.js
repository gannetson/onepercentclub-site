/**
 * Init
 * 
 * Put everything here that can't be handled by a $().live() thingy
 * 
 * 
 * @param {Object} container
 */
jQuery.fn.exists = function(){return this.length>0;}

function initBehaviour(container) {
    $("label.inline", container).inFieldLabels(); 
    $("textarea", container).autogrow();
    
    // initFileUpload();
    toggleText( $('.toggle-reactions', container) );
    toggleText( $('.toggle-love', container) );
    toggleText( $('#subtitle'), $('#logo', container) );
}

// Initializing
$(document).ready(function(){

    initProgress();
    //initLightbox();
    //initJiraFeedback();
    
    // show/hide reactions
    $('.toggle-reactions').live('click', function(e) {
        $('.reactions', $(this).closest('.reaction-box')).toggle();
    });
    
    // show/hide sharing options
    $('.share')
        .live('mouseenter', function(e) {
            $('.share-actions', $(this)).show();
        })
        .live('mouseleave', function(e) {
            $('.share-actions', $(this)).hide();
        });
    
    // DEVELOPMENT: needed for static template
    initPopup()
    initBehaviour('body');
    
    
});


// show popup on hover of element, styled and positioned by css. 
// Needed because we can't render elements outside parent with overview: hidden
// TODO IN PROGRESS 
function initPopup() {
    popupTimer = null;
    $('.member, .popup').live('mouseenter', function(e) {
        
        // if his has a .popup as child
        if( $('.popup', this).exists() ) {
            // hide & remove any previous popups
            $('.clone').fadeOut(40, function() {
                $(this).remove();
            });
            // clone to bottom of DOM & display
            $('.popup', this)
                .clone()
                .addClass('clone')
                .offset( $('.popup', this).offset() )
                .appendTo($('body'))
                .hide()
                .css('visibility', 'visible')
                .fadeIn(40);
        }
        // check if we have a pending execution and clear it if necessary
        if(popupTimer != null) {
            clearTimeout(popupTimer);
            popupTimer = null;
        }
    });
    // hide onmouseout of parent & popup iself. Needs timer for the later
    $('.member, .clone').live('mouseleave', function(e) {
        popupTimer = setTimeout(function() {
            $('.clone').fadeOut(40, function() {
                $(this).remove();
            });
        }, 200);
    });
};


// toggles content and classnames on click, mouseenter & mouseleave
// TODO: make generic
function toggleText(el, parent){
    // swap text & classnames
    parent = typeof parent !== 'undefined' ? parent : el;
    
    $(parent)
        .live('click',{el: el}, function(e, el) {
            $(el)
                .toggleClass('is-active')
                .addClass('is-activated')
                .trigger('mouseleave');
            e.preventDefault();
        })
        .live('mouseenter',{el: el}, function(e) {
            if ( $(el).hasClass('is-active') ) {
                $(el).html( $(el).data('content-toggled-hover') );
            } else {
                $(el).html( $(el).data('content-hover') );
            }
            $(el).removeClass('is-activated');
        })
        .live('mouseleave',{el: el}, function(e) {
            if ( $(el).hasClass('is-active') ) {
                $(el).html( $(el).data('content-toggled') );
            } else {
                $(el).html( $(el).data('content') );
            }
        });
};


// replace default file uploader with multiple file uploader
// TODO
function initFileUpload(){

    $('.fileupload').fileupload({

    });
}


// open external data in lightbox on specific links
// TODO: refactor
function initLightbox(){
 
    $('a.open-in-lightbox').live('click',function(e){

        $.colorbox({
            href: this.href,
            fixed: true,
            overlayClose: false,
            escKey: true,
            opacity: '0.7',
            scrolling: true,
            transition: 'none',
            width: 880,
            maxHeight: '90%',
            top: '40px',
            onComplete: function(){
                initInputCountdown('#colorbox');
            }
        });
            
        return false;
        e.preventDefault();
        
    });
    
    // custom lightbox close actions
    $("#lightbox-cancel, #lightbox-save").live("click", function(e){
        $.colorbox.close();
    });

    $(".loginbox").colorbox({
        fixed: true,
        overlayClose: false,
        escKey: true,
        opacity: '0.7',
        scrolling: false,
        transition: 'none',
        width: 400,
        height: 300,
        iframe: true
    });
    
    
}


// animate donation-progress meter
// TODO: refactor
function initProgress(){

    $('.donate-static').each(function(){
        var donated = Math.round($('.donated', this).html()); 
        var asked = Math.round($('.asked', this).html());
        if (donated > asked) {
            perc = 100;
        } else if (asked) {
            perc = 100 * donated / asked;
        } else {
            perc = 100;
        }
        perc = Math.round(perc);
        $('.donate-percentage', this).css({width: perc +'%'});
    });

    $('.donate-status').each(function(){
        var donated = Math.round($('.donated', this).html()); 
        var asked = Math.round($('.asked', this).html());
        if (donated > asked) {
            perc = 100;
        } else if (asked) {
            perc = 100 * donated / asked;
        } else {
            perc = 100;
        }
        perc = Math.round(perc);
        if (perc == 0) {
            $('.donate-percentage', this).addClass('is-empty');
        } else if(perc == 100) {
            $('.donate-percentage', this).addClass('is-full');
            
        } else {
            $('.donate-percentage', this).addClass('is-in-progress');
        }
        
        $('.donate-percentage', this).animate({width: perc +'%'}, 2000);
        
    });
}


// direct feedback into Jira
function initJiraFeedback() {
    jQuery.ajax({
        url: "https://onepercentclub.atlassian.net/s/en_USfyzlz7-418945332/809/42/1.2.5/_/download/batch/com.atlassian.jira.collector.plugin.jira-issue-collector-plugin:issuecollector-embededjs/com.atlassian.jira.collector.plugin.jira-issue-collector-plugin:issuecollector-embededjs.js?collectorId=8a8cc0df",
        type: "get",
        cache: true,
        dataType: "script"
    });
}
