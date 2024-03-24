$(function() {
    const selectedDate = $('#id_date').datepicker({
      format: 'dd.mm.yyyy',
      autoclose: true,
      orientation: 'bottom'
    });

    // Добавление обработчика события изменения даты
    $('#id_date').on('changeDate', function (e) {
      const selectedDate = e.date; // Получение выбранной даты
      console.log("Выбранная дата: " + selectedDate);
    });

    $.validator.addMethod("validDate", function(value, element) {
        return !/Invalid|NaN/.test(new Date(value));
    }, "Пожалуйста, введите корректную дату.");

    // Применяем валидацию к полю
    $('#id_date').rules("add", {
        validDate: true
    });

});
