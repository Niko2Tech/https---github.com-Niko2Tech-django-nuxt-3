export function addToCart(product) {
    // Obtener el carrito actual del local storage
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Verificar si el producto ya está en el carrito
    const existingProductIndex = cart.findIndex(item => item.id === product.id);

    if (existingProductIndex !== -1) {
        // Si el producto ya está en el carrito, aumentar la cantidad
        cart[existingProductIndex].quantity += 1;
    } else {
        // Si el producto no está en el carrito, agregarlo con cantidad 1
        product.quantity = 1;
        cart.push(product);
    }

    // Guardar el carrito actualizado en el local storage
    localStorage.setItem('cart', JSON.stringify(cart));
}

export function getCart() {
    return JSON.parse(localStorage.getItem('cart')) || [];
}

export function clearCart() {
    localStorage.removeItem('cart');
}

export function removeFromCart(productId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    const updatedCart = cart.filter(item => item.id !== productId);

    localStorage.setItem('cart', JSON.stringify(updatedCart));
}