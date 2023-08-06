const $ = require('jquery');

require('./markup.css');

function markupWidget(slice, payload) {
  $('#code').attr('rows', '15');
  slice.container.css({
    overflow: 'auto',
    height: '100%',
  });
  slice.container.html(payload.data.html);
}

module.exports = markupWidget;
