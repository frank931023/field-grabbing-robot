// 定義運動與地點的對應關係
const sportLocations = {
  籃球: ["室內籃球場A", "室內籃球場B"],
  羽球: [
    "羽球場07(依仁堂籃球館)",
    "羽球場08(依仁堂籃球館)",
    "羽球場09(依仁堂籃球館)",
    "羽球場10(依仁堂籃球館)",
    "羽球場11(依仁堂籃球館)",
    "羽球場12(依仁堂籃球館)",
  ],
  排球: ["室內排球場-(男網)", "室內排球場-(女網)"],
  桌球: [
    "桌球場01",
    "桌球場02",
    "桌球場03",
    "桌球場04",
    "桌球場05",
    "桌球場06",
    "桌球場07",
    "桌球場08",
    "桌球場09",
    "桌球場10",
  ],
  網球: ["操你媽沒有網球場可以借"],
};

// 時間範圍
const startTime = 9;
const endTime = 22;

// 生成多選時間的選項
function generateTimeOptions() {
  const timeContainer = document.getElementById("time");
  for (let i = startTime; i <= endTime; i++) {
    const timeLabel = document.createElement("label");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = `${i}:00`;
    timeLabel.appendChild(checkbox);
    timeLabel.appendChild(document.createTextNode(`${i}:00`));
    timeContainer.appendChild(timeLabel);
  }
}

// 根據選擇的運動動態更新地點選項
document.getElementById("sport").addEventListener("change", function () {
  const sport = this.value;
  const locationSelect = document.getElementById("location");
  locationSelect.innerHTML = ""; // 清空選項

  if (sport && sportLocations[sport]) {
    sportLocations[sport].forEach((location) => {
      const option = document.createElement("option");
      option.value = location;
      option.textContent = location;
      locationSelect.appendChild(option);
    });
  } else {
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "請先選擇運動";
    locationSelect.appendChild(defaultOption);
  }
});

// 確認按鈕點擊事件
document.getElementById("confirmButton").addEventListener("click", function () {
  const date = document.getElementById("date").value;
  const sport = document.getElementById("sport").value;
  const location = document.getElementById("location").value;
  const selectedTimes = Array.from(
    document.querySelectorAll("#time input[type='checkbox']:checked")
  ).map((checkbox) => checkbox.value);

  if (!date || !sport || !location || selectedTimes.length === 0) {
    alert("請填寫所有欄位！");
    return;
  }

  // 顯示成功訊息
  alert(
    `預約成功！\n日期：${date}\n運動：${sport}\n場地：${location}\n時間：${selectedTimes.join(
      ", "
    )}`
  );

  // 重置表單
  document.getElementById("reservationForm").reset();

  // 清除選中的時間
  document
    .querySelectorAll("#time input[type='checkbox']")
    .forEach((checkbox) => {
      checkbox.checked = false;
    });

  // 重置地點選項
  document.getElementById("location").innerHTML =
    "<option value=''>請先選擇運動</option>";
});

// 初始化時間選項
generateTimeOptions();
