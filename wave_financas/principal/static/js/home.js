function showSubMenu(id)
{
    var subMenu = document.getElementById(id);
    if (subMenu.style.display === "block") {
        subMenu.style.display = "none";
    } else {
        subMenu.style.display = "block";
    }
}
function hideContainers()
{
    const cardsContainer = document.querySelector('.cards-container');
    const dashboardContainer = document.querySelector('.dashboard-container');

    if (cardsContainer) {
        cardsContainer.style.display = 'none';
    }

    if (dashboardContainer) {
        dashboardContainer.style.display = 'none';
    }
}