from IPython.display import HTML

hide_me = ''

HTML('''
<style>
    .container {
        box-shadow: none !important;
    }

    .output_html {
        shadow: none !important;
        max-width: 100% !important;
        padding: 0 !important;
    }

    .title1 {
        color: #e74a49 !important;
    }
</style>

<script async>
code_show=true;
function code_toggle() {
  if (code_show) {
    $('div.input').each(function(id) {
      el = $(this).find('.cm-variable:first');
      if (id == 0 || el.text() == 'hide_me') {
        $(this).hide();
      }
    });
    $('div.output_prompt').css('opacity', 0);
  } else {
    $('div.input').each(function(id) {
      $(this).show();
    });
    $('div.output_prompt').css('opacity', 1);
  }
  code_show = !code_show
}
$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input style="opacity:0" type="submit" value="Click here to toggle on/off the raw code."></form>''')
