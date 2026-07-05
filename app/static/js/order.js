document.getElementById('sendOrderBtn').addEventListener('click', function () {
    const clientName = document.getElementById('clientName').value.trim();
    if (clientName) {
        fetch('/order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: clientName, items: cartItems })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Order sent successfully!');
                    location.reload();
                } else {
                    alert('Failed to send order. Please try again.');
                }
            })
            .catch(error => {
                alert(error);
            });
    } else {
        alert('Please enter your name before sending the order.');
    }
});

document.getElementById('clearCartBtn').addEventListener('click', function () {
    if (confirm('Are you sure you want to clear the cart?')) {
        fetch('/clear_cart', {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Cart cleared successfully!');
                    location.reload();
                } else {
                    alert('Failed to clear cart. Please try again.');
                }
            })
            .catch(error => {
                alert(error);
            });
    }
});

document.querySelectorAll('.remove-item-btn').forEach(button => {
    button.addEventListener('click', function () {
        const Iditem = this.getAttribute('data-item-id');
        if (confirm('Are you sure you want to remove this item from the cart?')) {
            fetch('/remove_item', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id_item: Iditem })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Item removed successfully!');
                        location.reload();
                    } else {
                        alert('Failed to remove item. Please try again.');
                    }
                })
                .catch(error => {
                    alert(error);
                });
        }
    });
});
