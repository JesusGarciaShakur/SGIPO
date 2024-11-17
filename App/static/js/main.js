$(document).ready(function () {

	/*  Show/Hidden Submenus */
	$('.nav-btn-submenu').on('click', function (e) {
		e.preventDefault();
		var SubMenu = $(this).next('ul');
		var iconBtn = $(this).children('.fa-chevron-down');
		if (SubMenu.hasClass('show-nav-lateral-submenu')) {
			$(this).removeClass('active');
			iconBtn.removeClass('fa-rotate-180');
			SubMenu.removeClass('show-nav-lateral-submenu');
		} else {
			$(this).addClass('active');
			iconBtn.addClass('fa-rotate-180');
			SubMenu.addClass('show-nav-lateral-submenu');
		}
	});

	/*  Show/Hidden Nav Lateral */
	$('.show-nav-lateral').on('click', function (e) {
		e.preventDefault();
		var NavLateral = $('.nav-lateral');
		var PageConten = $('.page-content');
		if (NavLateral.hasClass('active')) {
			NavLateral.removeClass('active');
			PageConten.removeClass('active');
		} else {
			NavLateral.addClass('active');
			PageConten.addClass('active');
		}
	});
	// Obtener elementos
	const exitButton = document.querySelector('.btn-exit-system');
	const modal = document.getElementById('exitModal');
	const cancelButton = document.getElementById('cancelExit');
	const confirmButton = document.getElementById('confirmExit');

	// Mostrar el modal cuando se hace click en el botón de salir
	exitButton.addEventListener('click', (e) => {
		e.preventDefault();
		modal.classList.add('show');
	});

	// Cerrar el modal cuando se cancela
	cancelButton.addEventListener('click', () => {
		modal.classList.remove('show');
	});

	// Confirmar la salida (puedes poner la URL de logout aquí)
	confirmButton.addEventListener('click', () => {
		window.location.href = '/logout'; // Cambia esto con la URL de logout real
	});
});

(function ($) {
	$(window).on("load", function () {
		$(".page-content, .nav-lateral-content").mCustomScrollbar({
			theme: "light-thin",
			scrollbarPosition: "inside",
			autoHideScrollbar: true,
			scrollButtons: { enable: true }
		});
	});
})(jQuery);