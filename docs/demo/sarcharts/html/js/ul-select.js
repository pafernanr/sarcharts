$.fn.ulSelect = function(callback){
  var ul = $(this);
  // Add a div before the <ul> to hold the selected text
  ul.before('<div class="selected--zg-ul-select"></div>');
  // Store that div
  var selected = ul.prev();

  if (!ul.hasClass('zg-ul-select')) {
    ul.addClass('zg-ul-select');
  }
  $(this).on('click', 'li', function(){
    // hide selected
    selected.hide();
    // Toggle active class on the <ul>
    ul.toggleClass('active');
    // Remove active class from any <li> that has it...
    ul.children().removeClass('active');
    // And add the class to the <li> that gets clicked
    $(this).toggleClass('active');
    // The text of the click <li>
    var selectedText = $(this).html();
    // If the <ul> dropdown is open, activate the selected, and append the clicked <li> text (and SVG arrow)
    if (ul.hasClass('active')) {
      selected.html(selectedText).addClass('active');
    }
    else {
      // Remove selected
      selected.html('').removeClass('active');
      callback(this);
    }
    });
    // Close the faux select menu when clicking outside it
    $(document).on('click', function(event){
      if(ul.length) {
       if(!ul.has(event.target).length == 0) {
        return;
      }
      else {
        ul.removeClass('active');
        selected.removeClass('active').html('');
      }
    }
  });
}
