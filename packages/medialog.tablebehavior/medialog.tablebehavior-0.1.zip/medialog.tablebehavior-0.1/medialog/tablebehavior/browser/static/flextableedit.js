<script type="text/javascript">
$(function () {
    var contentArray = [
        ["Year", "Ford", "Volvo", "Toyota", "Honda", "Remark"],
        ["2014", 10, 11, 12, 13, '-'],
        ["2015", 20, 11, 14, 13, "Boston's figures"],
        ["2016", 30, 15, 12, 13, 'Checked: "7"']
    ];
    $('#sometable').flextabledit({
      content: contentArray,
      addTableClass: "myTable"
    });
  });
</script>