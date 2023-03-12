let showBtn = document.querySelector(".btn__show-history");
let historyCards = document.querySelector(".historyOrder");
let btnClose = document.querySelector(".btn__close");


showBtn.addEventListener("click", function () {
  showBtn.classList.toggle("btn__show-history_HIDDEN");
  historyCards.classList.toggle("historyOrder_ACTIVE");
});

btnClose.addEventListener("click", function () {
  showBtn.classList.remove("btn__show-history_HIDDEN");
  historyCards.classList.remove("historyOrder_ACTIVE");
});
