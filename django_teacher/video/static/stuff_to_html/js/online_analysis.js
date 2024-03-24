$(function() {

    const timerElement = document.getElementById('timer');
    const loadTime = timerElement.getAttribute('data-load-time');
    const startTime = new Date(loadTime);


    function stopTimer() {
        clearInterval(timerInterval); // Остановить интервал таймера
    }
    function updateTimer() {
      const now = new Date();
      const elapsedTime = now - startTime;
      const hours = Math.floor(elapsedTime / 3600000);
      const minutes = Math.floor((elapsedTime % 3600000) / 60000);
      const seconds = Math.floor((elapsedTime % 60000) / 1000);

      const timeString = `Видео длится: ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

      timerElement.textContent = timeString;
    }

    const timerInterval = setInterval(updateTimer, 1000);
    updateTimer();


    document.getElementById("videoForm").addEventListener("submit", function(event) {
        stopTimer();

        const timerElement = document.getElementById('timer');
        const loadTime = new Date().toISOString();
        const startTime = new Date(loadTime);

        function updateTimer() {
          const now = new Date();
          const elapsedTime = now - startTime;
          const hours = Math.floor(elapsedTime / 3600000);
          const minutes = Math.floor((elapsedTime % 3600000) / 60000);
          const seconds = Math.floor((elapsedTime % 60000) / 1000);

          const timeString = `Видео брабатывается: ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

          timerElement.textContent = timeString;
        }

        const timerInterval = setInterval(updateTimer, 1000);

        updateTimer();
  });

});
