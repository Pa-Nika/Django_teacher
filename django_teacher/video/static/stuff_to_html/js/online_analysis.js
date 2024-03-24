$(function() {

    const timerElement = document.getElementById('timer');
    const loadTime = timerElement.getAttribute('data-load-time');
    const startTime = new Date(loadTime);


    function updateTimer() {
      const now = new Date();
      const elapsedTime = now - startTime;
      const hours = Math.floor(elapsedTime / 3600000);
      const minutes = Math.floor((elapsedTime % 3600000) / 60000);
      const seconds = Math.floor((elapsedTime % 60000) / 1000);

      // Формируем строку для отображения времени
      const timeString = `Видео длится: ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

      // Обновляем содержимое элемента таймера
      timerElement.textContent = timeString;
    }

    const timerInterval = setInterval(updateTimer, 1000);
    updateTimer();
});
