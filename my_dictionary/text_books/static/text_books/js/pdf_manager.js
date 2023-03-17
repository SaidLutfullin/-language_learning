$(document).ready(function($) {


    const keysBookUrl = $("#keysBookUrl").val();
    const url = $("#textBookUrl").val();

    let loadingTask = pdfjsLib.getDocument(url)

    let pdfDoc = null;
    let keysPdfDoc = null;

    const pageNumberInput = $("#pageNumberInput");
    const keysPageNumberInput = $("#keysPageNumberInput");



    let lastPage = null;
    let lastKeyPage = null;

    loadingTask.promise.then(pdf => {
        pdfDoc = pdf
        lastPage = pdfDoc.numPages;
        goToPage ()

        if (keysBookUrl == "") {
            keysPdfDoc = pdfDoc
            lastKeyPage = lastPage
            goToKeyPage()
        } else {
            loadingTask = pdfjsLib.getDocument(keysBookUrl)
            loadingTask.promise.then(pdf => {
                keysPdfDoc = pdf
                lastKeyPage = keysPdfDoc.numPages;
                goToKeyPage ()
            });
        }
    });


    function renderPage (pageNumber) {
          // load page
          pdfDoc.getPage(pageNumber).then(function(page) {
                // scale the page
                const scale = parseFloat($("#scale").val())/100

                const viewport = page.getViewport({ scale: scale });

                // creating canvas
                const canvas = document.getElementById('pdf-canvas')

                const context = canvas.getContext('2d');
                canvas.height = viewport.height;
                canvas.width = viewport.width;
                page.render({ canvasContext: context, viewport: viewport });
          });
    }

    function renderKeysPage (pageNumber) {
          // load page
          keysPdfDoc.getPage(pageNumber).then(function(page) {
                // scale the page
                const scale = parseFloat($("#keys-scale").val())/100
                const viewport = page.getViewport({ scale: scale });

                // creating canvas
                const canvas = document.getElementById('keys-pdf-canvas')

                const context = canvas.getContext('2d');
                canvas.height = viewport.height;
                canvas.width = viewport.width;
                page.render({ canvasContext: context, viewport: viewport });
          });
    }

    // UI functionality

    $("#goForwardButton").click(function(){
        goToPage(false, true)
    });

    $("#goBackButton").click(function(){
        goToPage(true, false)
    });

    $("#goButton").click(function(){
        goToPage()
    });
    // keys book
    $("#keysGoForwardButton").click(function(){
        goToKeyPage(false, true)
    });

    $("#keysGoBackButton").click(function() {
        goToKeyPage(true, false)
    });

    $("#keysGoButton").click(function(){
        goToKeyPage()
    });

    $('#pageNumberInput').keypress(function (e) {
        let key = e.which;
        if(key == 13) {
            goToPage()
        }
    });

    $('#keysPageNumberInput').keypress(function (e) {
        let key = e.which;
        if(key == 13) {
            goToKeyPage()
        }
    });

    function goToPage (previous=false, next=false) {
        let current_page = parseInt( pageNumberInput.val());
        if (previous) {
            current_page--
        } else if (next) {
            current_page++
        }
        if (current_page<1) {
            current_page=1
        }
        else if (current_page>lastPage) {
            current_page=lastPage
        }
        pageNumberInput.val(current_page)
        renderPage(current_page);
    }

    function goToKeyPage (previous=false, next=false) {
        let current_page = parseInt( keysPageNumberInput.val());
        if (previous) {
            current_page--
        } else if (next) {
            current_page++
        }
        if (current_page<1) {
            current_page=1
        }
        else if (current_page>lastKeyPage) {
            current_page=lastKeyPage
        }
        keysPageNumberInput.val(current_page)
        renderKeysPage(current_page);
    }


    // keys panel UI
    $("#showKeys").click(function(){
        $("#keys-block").addClass('full-block');
        $("#keys-block").removeClass('hiden');

        $("#text-book-block").addClass('hiden');
        $("#text-book-block").removeClass('full-block');

        $("#splitKeys").removeClass('hiden');
    });

    $("#hideKeys").click(function(){
        $("#text-book-block").addClass('full-block');
        $("#text-book-block").removeClass('hiden');

        $("#keys-block").addClass('hiden');
        $("#keys-block").removeClass('full-block');

        $("#splitKeys").removeClass('hiden');
    });

    $("#splitKeys").click(function(){
        $("#keys-block").removeClass('full-block');
        $("#text-book-block").removeClass('hiden');

        $("#keys-block").addClass('half-block');
        $("#text-book-block").addClass('half-block');

        $("#splitKeys").addClass('hiden');
    });

    // scale
    $('#scale').keypress(function (e) {
        let key = e.which;
        if(key == 13) {
            goToPage()
        }
    });

    $('#keys-scale').keypress(function (e) {
        let key = e.which;
        if(key == 13) {
            goToKeyPage()
        }
    });

    // send form
    $("#saveExercise").click(function(){
        const formPageNumber = $("#id_page_number")
        const formKeysPageNumber = $("#id_keys_page_number")
        formPageNumber.val(pageNumberInput.val())
        formKeysPageNumber.val(keysPageNumberInput.val())
        $("#exerciseForm").submit();
    });

});