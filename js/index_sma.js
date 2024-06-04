document.getElementById('form').addEventListener('submit', function(e) {
    e.preventDefault();
    var sma_action = document.getElementById('sma_action').value;
    var sma_start_date = document.getElementById('sma_start_date').value;
    var sma_signal_bottom = document.getElementById('sma_signal_bottom').value;
    var sma_signal_top = document.getElementById('sma_signal_top').value;
    var sma_wallet_start = document.getElementById('sma_wallet_start').value;
    // Ici, vous pouvez utiliser les valeurs pour modifier le fichier algoV1.py
    console.log(sma_action, sma_start_date, sma_signal_bottom, sma_signal_top, sma_wallet_start);
});


