function refreshSet(callingelement, target) {
    $.ajax({
        method: 'GET',
        url: '/profile/refresh?what='+target+'&'+callingelement.id+'='+callingelement.value,
        dataType: 'text',
        success: function (text) { $('#'+target+'span').html(text); }
    });
}

$(document).ready(function() {
    $(".popup_iframe").fancybox({
        'width': 440,
        'transitionIn': 'none',
        'transitionOut': 'none',
        'type': 'iframe',
        'scrolling': 'no'
    });

    $('ul.menu li.head').each(function () {
        var speed = 'fast';
        $(this).hoverIntent(
            function () {
                $('div', this).slideDown(speed);
                $('a', this).eq(0).css('background-image', 'url(/img/menu_pointer_hover.gif)');
            },
            function () {
                $('div', this).slideUp(speed);
                $('a', this).eq(0).css('background-image', 'url(/img/menu_pointer.gif)');
            }
        );
    });
    $('ul.menu .submenu-container a').hover(
        function () {
            $(this).parents('li').eq(0).addClass('hover');
        },
        function () {
            $(this).parents('li').eq(0).removeClass('hover');
    });
});

function filterMe(element) {
    $(element).parents('form').eq(0).submit();
}

function alignBlocks() {
    bllogin = $('.block.inlog');
    blpoll = $('.block.special');
    blrefs = $('.block.refs');

    offset = Math.max(bllogin.outerHeight(true) + bllogin.position().top,
                    blpoll.outerHeight(true) + blpoll.position().top,
                    blrefs.outerHeight(true) + blrefs.position().top);

    bllogin.css('margin-top', (offset - bllogin.outerHeight() - bllogin.position().top) + 'px');
    blpoll.css('margin-top', (offset - blpoll.outerHeight() - blpoll.position().top) + 'px');
    blrefs.css('margin-top', (offset - blrefs.outerHeight() - blrefs.position().top) + 'px');
}

/** Header **/

/**
 * Rotates the text-images and fades in the face on the first time visit of the homepage.
 *
 * This has a high chance of making the website one large circus. Be careful.
 * Also, this method eats memory with the cycling of things and nested methods. Proposal for change:
 * 1) get one (1) method, that executes _all_ actions, at set times.
 * 2) window.setinterval() instead of hundreds of calls to settimeout.
 * 3) keep an external counter how many seconds passed since the first step. Reset at end of last step.
 */
function cycleImages(order) {
    // Prepare
    $('.visual img').hide();

    firstFadeIn = 1000;
    fadeInms = 1500;
    fadeOutms = 1500;
    fadePauze = 2000;
    fadePauze2 = 7000;
    fadePauze3 = 1000;
    numHeaders = 4;
    var cycle = true;
    var useorder = order;

    // Cycle methods.

    var alterSourceFiles = function() {
        // Grab current set (1, .., 4)
        curHeader = parseInt($('.visual-face').get(0).src.match(/header-([0-9])/)[1]);
        inof = useorder.indexOf(curHeader);
        if (useorder.length == inof+1) {
            next = useorder[0];
        }
        else {
            next = useorder[inof+1];
        }

        var replaceHeader = function (element, num) {
            return element.src.replace(/header-[0-4]/, 'header-'+num);
        }

        $('.visual-face').attr('src', replaceHeader($('.visual-face').get(0), next));
        $('.visual-text-name').attr('src', replaceHeader($('.visual-text-name').get(0), next));
        $('.visual-text-1').attr('src', replaceHeader($('.visual-text-1').get(0), next));
        $('.visual-text-2').attr('src', replaceHeader($('.visual-text-2').get(0), next));
        $('.visual-text-3').attr('src', replaceHeader($('.visual-text-3').get(0), next));

        fadeInFace();
        fadeInText1();
        fadeInName(false);
    }

    var fadeOutText3 = function () {
        $('.visual-text-3').fadeOut(fadeOutms);
        $('.visual-face').fadeOut(fadeOutms);
        $('.visual-text-name').fadeOut(fadeOutms);
        window.setTimeout(alterSourceFiles, fadeOutms);
    }
    var fadeInText3 = function () {
        $('.visual-text-3').fadeIn(fadeInms);
        window.setTimeout(fadeOutText3, fadePauze2 + fadeInms);
    }
    var fadeOutTexts = function () {
        $('.visual-text-1').fadeOut(fadeOutms);
        $('.visual-text-2').fadeOut(fadeOutms);
        window.setTimeout(fadeInText3, fadeOutms);
    }
    var fadeInText2 = function () {
        $('.visual-text-2').fadeIn(fadeInms);
        window.setTimeout(fadeOutTexts, fadePauze2 + fadeInms)
    }
    var fadeInText1 = function (slow) {
        speed = !slow?fadeInms:firstFadeIn
        $('.visual-text-1').fadeIn(speed);
        window.setTimeout(fadeInText2, fadePauze + speed)
    }
    var fadeInName = function(first) {
        $('.visual-text-name').fadeIn(firstFadeIn);
        if (first) {
            window.setTimeout(fadeInText1, fadePauze3 + firstFadeIn);
        }
    }
    var fadeOutName = function () {
        $('.visual-text-name').fadeOut(fadeOutms);
    }
    var fadeInFace = function() {
        $('.visual .visual-face').fadeIn(firstFadeIn);
    }

    fadeInFace();
    fadeInName(true);
}

/** Carrousel **/

var references = new Array();
var carrouselStep = 0;
var curreference = 0;

function initCarrousel(ident) {
    elm = $(ident)

    // find all refs
    elm.find('.reference').each(function () {
        // Add to general list
        references.push($(this));

        // Align the img in the center
        img = $('img', this);
        img.css('margin-top', ($(this).innerHeight() - img.outerHeight()) / 2 + 'px');

        // Hide it
        $(this).hide()
    });

    width = elm.find('.scrollbar').eq(0).innerWidth();
    slider = elm.find('.slider').eq(0).outerWidth();
    carrouselStep = (width - slider) / (references.length-1);

    // Apply hooks to .left and .right
    elm.find('.left').click(function () {
        slidecarrouselLeft();
    });
    elm.find('.right').click(function () {
        slidecarrouselRight();
    });

    // Apply drag-hook to .slider
    elm.find('.slider').draggable({
        axis: 'x',
        drag: function (event, ui) {
            dragcarrousel(event, ui)
        },
        containment: 'parent'
        });

    // Display first few
    if (references.length > 1) {
        for (var i=0;i<references.length;i++) {
            // Wat nu?
        }
    }
    curreference = 0;           // randomize this for random first-image
    drawcarrousel(curreference);

    // set window interval for animation
    window.setInterval(animateCarrousel, 5000);
}

function slidecarrouselLeft() {
    actCarrousel(curreference-1);
}

function slidecarrouselRight() {
    actCarrousel(curreference+1);
}

function slidecarrousel(toImage) {
    target = carrouselStep * toImage;
    $('.references .slider').animate({'left': target+'px'}, 1000, 'swing');
}

function dragcarrousel(event, ui) {
    slider = $(ui.helper.context)
    myPosition = ui.offset.left;
    parentPosition = slider.parents('div').eq(0).offset().left;
    newPosition = myPosition - parentPosition;
    curreference = Math.floor(newPosition / carrouselStep);
    drawcarrousel(newPosition);
}

function drawcarrousel(pos) {
    for (var i=0;i<references.length;i++) { references[i].hide(); }

    Cfocus = Math.floor(pos / carrouselStep);
    focusImage = references[Cfocus];
    focusImage.show();
}

function actCarrousel(toPos) {
    references[curreference].fadeOut('fast', function () {
        curreference = toPos;
        if (curreference >= references.length) {
            curreference = 0;
        }
        if (curreference < 0) {
            curreference = references.length-1;
        }
        references[curreference].fadeIn('fast');
        slidecarrousel(curreference);
    });
}

function animateCarrousel() {
    actCarrousel(curreference+1);
}

/** Form support */

function loadFunctions(element) {
    $.ajax({
        url: '/support/loadFunctions?group='+element.value,
        dataType: 'json',
        success: function (data) {
            // Clear sibling select 'function', except for the default ("") value
            funcselect = 0;
            if (element.name.match(/_runnerup$/)) {
                funcselect = $(element).siblings('select[name=function_runnerup]').eq(0)
            }
            else {
                funcselect = $(element).siblings('select[name=function]').eq(0)
            }
            
            funcselect.find('option').each(function () {
                if (this.value != '') {
                    $(this).remove();
                }
            })

            for (var i=0;i<data.functions.length;i++) {
                func = data.functions[i];
                funcselect.append('<option value="'+ func.id +'">'+ func.title +'</option>');
            }
        }
    });
}

function loadDesc(element) {
    $.ajax({
        url: '/support/loadDescription/' + element.value,
        dataType: 'json',
        success: function(data) {
            $('#help_functie p').html(data.description);
            $('#help_functie').show();
        }
    });
}

/** Candidate hover methods **/

function showExtra(element, e) {
    extr = $(element).siblings('.extra-info').eq(0);
    extr.css('left', (e.pageX+10) + 'px')
    extr.css('top', (e.pageY) + 'px')
    extr.show();
}

function hideExtra(element, e) {
    extr = $(element).siblings('.extra-info').eq(0);
    extr.hide();
}

/** Route **/

function init_map(from, to)
{
    $('#route-canvas').html('');
    directionsDisplay = new google.maps.DirectionsRenderer();
    var rotterdam = new google.maps.LatLng(51.914193,4.475797);
    var myOptions = {
        zoom:16,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        center: rotterdam
    }
    map = new google.maps.Map($('#route-canvas').get(0), myOptions);
    directionsDisplay.setMap(map);
    directionsDisplay.setPanel($('#route-itinerary').get(0));

    srch = window.location.search
    if (srch.match(/workarea=/) && srch.match(/postcode=/)) {
        refreshMap($('#route-form').get(0));
    }
}

function refreshMap(form) {
    address = {'1': 'Keizersgracht 592, Amsterdam, Netherlands', '2': 'Eendrachtsweg 42, Rotterdam, Netherlands'}
    var start = $('#postcode').val();
    var end = address[$('#workarea').val()];
    var request = {
        origin:start,
        destination:end,
        travelMode: google.maps.DirectionsTravelMode.DRIVING
    };
    directionsService.route(request, function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
        }
    });
    return false;
}