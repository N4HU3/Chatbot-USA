// Efecto input
const inputs = document.querySelectorAll(".input-form"); // Seleccionar todas las entradas de form por su clase
inputs.forEach(input => {
    input.onfocus = () => {
        input.previousElementSibling.classList.add("top");
        input.previousElementSibling.classList.add("focus");
        input.parentNode.classList.add("focus");
    }
    input.onblur = () => {
        input.value = input.value.trim();
        if (input.value.trim().length == 0) { // Si no hay contenido, se remueve la clase "top"
            input.previousElementSibling.classList.remove("top");
        }
        input.previousElementSibling.classList.remove("focus");
        input.parentNode.classList.remove("focus");
    }
});

// Envío de datos de formulario por medio del botón "Iniciar atención"
document.getElementById("btn-new-conv").addEventListener("click", async function (event) {
    event.preventDefault();

    // Obtener los valores de los campos del formulario
    var name = document.getElementById("name").value; // Nombre
    var mail = document.getElementById("mail").value; // Correo Electrónico
    var confAttention = document.getElementById("checkConfAttention"); // Checkbox de aceptación

    // Validaciones: Nombre
    if (name === "") {
        document.getElementById("warning-text-name").classList.add("warning-text-visible");
        document.getElementById("name").classList.add("warning");
        document.getElementById("span-name").classList.add("warning-span");
        return;
    } else {
        document.getElementById("name").classList.remove("warning");
        let warnName = document.getElementById("warning-text-name");
        warnName.style.display = "none";
        document.getElementById("span-name").classList.remove("warning-span");
    }

    // Validaciones: Correo Electrónico - Campo vacío
    if (mail === "") {
        document.getElementById("warning-text-mail").classList.add("warning-text-visible");
        document.getElementById("mail").classList.add("warning");
        document.getElementById("span-mail").classList.add("warning-span");
        return;
    } else {
        document.getElementById("mail").classList.remove("warning");
        let warnEmail = document.getElementById("warning-text-mail");
        warnEmail.style.display = "none";
        document.getElementById("span-mail").classList.remove("warning-span");
    }

    // Validaciones: Correo Electrónico - Caracteres inválidos
    var mailRegex = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    if (!mailRegex.test(mail)) {
        document.getElementById("warning-invalid-mail").classList.add("warning-text-visible");
        document.getElementById("mail").classList.add("warning");
        document.getElementById("span-mail").classList.add("warning-span");
        return;
    } else {
        document.getElementById("mail").classList.remove("warning");
        let warnInvalid = document.getElementById("warning-invalid-mail");
        warnInvalid.style.display = "none";
        document.getElementById("span-mail").classList.remove("warning-span");
    }

    // Validación: Confirmación de atención (checkbox)
    if (!confAttention.checked) {
        document.getElementById("warning-text-checkConfAttention").classList.add("warning-text-visible");
        document.getElementById("checkConfAttention").classList.add("warning-checkbox");
        return;
    } else {
        document.getElementById("warning-text-checkConfAttention").classList.remove("warning-text-visible");
        document.getElementById("checkConfAttention").classList.remove("warning-checkbox");
    }

    // Preparar parámetros comunes para la redirección
    let params = `name=${encodeURIComponent(name)}&mail=${encodeURIComponent(mail)}`;

    // Redirección a la URL de login con los parámetros incluidos
    window.location.href = "/?" + params;
});
