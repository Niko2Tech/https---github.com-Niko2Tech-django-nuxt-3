export async function addToCart(product) {
    // Primero, intentamos descontar el stock en el backend
    try {
        const response = await fetch('http://127.0.0.1:8000/api/pedido/descontar_stock/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                producto: product.id,
                cantidad: 1
            })
        });

        const data = await response.json();

        if (!response.ok) {
            console.error('Error al descontar stock:', data.error);
            return data.error; // Retornar el mensaje de error al usuario
        } else {
            console.log('Stock descontado exitosamente:', data);

            // Si el descuento de stock fue exitoso, actualizamos el carrito
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
            return null;
        }
    } catch (error) {
        console.error('Error en la petición:', error);
    }
}

export async function removeFromCart(productId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Obtener el producto que se está eliminando
    const product = cart.find(item => item.id === productId);
    const productQuantity = product ? product.quantity : 0;

    // Actualizar el stock en el backend solo si el producto existe en el carrito
    if (productQuantity > 0) {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/pedido/agregar_stock/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    producto: productId,
                    cantidad: productQuantity
                })
            });

            const data = await response.json();

            if (!response.ok) {
                console.error('Error al agregar stock:', data.error);
                return data.error; // Retornar el mensaje de error al usuario
            } else {
                console.log('Stock agregado exitosamente:', data);

                // Si el stock fue agregado exitosamente, actualizamos el carrito
                const updatedCart = cart.filter(item => item.id !== productId);

                // Guardar el carrito actualizado en el local storage
                localStorage.setItem('cart', JSON.stringify(updatedCart));
            }
            return null;
        } catch (error) {
            console.error('Error en la petición:', error);
        }
    }
}

export async function removeSingleProductFromCart(productId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Obtener el producto que se está eliminando
    const product = cart.find(item => item.id === productId);

    // Actualizar el stock en el backend solo si el producto existe en el carrito
    if (product && product.quantity > 0) {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/pedido/agregar_stock/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    producto: productId,
                    cantidad: 1
                })
            });

            const data = await response.json();

            if (!response.ok) {
                console.error('Error al agregar stock:', data.error);
                return data.error; // Retornar el mensaje de error al usuario
            } else {
                console.log('Stock agregado exitosamente:', data);

                // Si el stock fue agregado exitosamente, actualizamos el carrito restándole 1 a la cantidad
                const updatedCart = cart.map(item => {
                    if (item.id === productId) {
                        return { ...item, quantity: item.quantity - 1 };
                    }
                    return item;
                }).filter(item => item.quantity > 0);

                // Guardar el carrito actualizado en el local storage
                localStorage.setItem('cart', JSON.stringify(updatedCart));

                return null;
            }
        }
        catch (error) {
            console.error('Error en la petición:', error);
        }
    }
}


export function getCart() {
    return JSON.parse(localStorage.getItem('cart')) || [];
}

export function clearCart() {
    localStorage.removeItem('cart');
}
