let array = Array.from({ length: 200 }, () => Math.floor(Math.random() * 100));
const container = document.getElementById("array-container");
const algorithmSelect = document.getElementById("algorithm");
const speedSelect = document.getElementById("speed");
const startResetButton = document.getElementById("start-reset-button");
let sortingInProgress = false;
let sortTimeouts = [];

function displayArray(arr, activeIndex = null) {
  container.innerHTML = "";
  arr.forEach((value, index) => {
    const bar = document.createElement("div");
    bar.style.height = value * 4 + "px";
    bar.className = "bar";
    if (index === activeIndex) {
      bar.classList.add("active");
    }
    container.appendChild(bar);
  });
}

function sleep(ms) {
  return new Promise((resolve) => {
    const timeout = setTimeout(resolve, ms);
    sortTimeouts.push(timeout);
  });
}

async function startSort() {
  if (sortingInProgress) {
    resetSort();
    return;
  }

  algorithmSelect.disabled = true;
  speedSelect.disabled = true;
  startResetButton.textContent = "Stop";
  startResetButton.classList.add("reset");
  sortingInProgress = true;

  const algorithm = algorithmSelect.value;
  const speed = parseInt(speedSelect.value);
  const response = await fetch("/sort", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ array, algorithm }),
  });
  const result = await response.json();
  for (const step of result.steps) {
    if (!sortingInProgress) break;
    const [currentArray, activeIndex] = step;
    displayArray(currentArray, activeIndex);
    await sleep(speed);
  }
  if (sortingInProgress) {
    displayArray(result.sorted_array);
    alert(`Sorting completed in ${result.duration.toFixed(4)} seconds`);
  }
  algorithmSelect.disabled = false;
  speedSelect.disabled = false;
  startResetButton.textContent = "Start Sort";
  startResetButton.classList.remove("reset");
  sortingInProgress = false;
}

function resetSort() {
  sortingInProgress = false;
  sortTimeouts.forEach((timeout) => clearTimeout(timeout));
  sortTimeouts = [];
  array = Array.from({ length: 200 }, () => Math.floor(Math.random() * 100));
  displayArray(array);
  algorithmSelect.disabled = false;
  speedSelect.disabled = false;
  startResetButton.textContent = "Start Sort";
  startResetButton.classList.remove("reset");
}

displayArray(array);

// Additional JS for floating balls
// const colors = ["#3CC157", "#2AA7FF", "#1B1B1B", "#FCBC0F", "#F85F36"];
const colors = ["#3CC157"];
const numBalls = 50;
const balls = [];
const ballContainer = document.getElementById("ball-container");

for (let i = 0; i < numBalls; i++) {
  let ball = document.createElement("div");
  ball.classList.add("ball");
  ball.style.background = colors[Math.floor(Math.random() * colors.length)];
  ball.style.left = `${Math.floor(Math.random() * 100)}vw`;
  ball.style.top = `${Math.floor(Math.random() * 100)}vh`;
  ball.style.transform = `scale(${Math.random()})`;
  ball.style.width = `${Math.random()}em`;
  ball.style.height = ball.style.width;

  balls.push(ball);
  ballContainer.append(ball);
}

// Keyframes
balls.forEach((el, i, ra) => {
  let to = {
    x: Math.random() * (i % 2 === 0 ? -11 : 11),
    y: Math.random() * 12,
  };

  let anim = el.animate(
    [
      { transform: "translate(0, 0)" },
      { transform: `translate(${to.x}rem, ${to.y}rem)` },
    ],
    {
      duration: (Math.random() + 1) * 2000, // random duration
      direction: "alternate",
      fill: "both",
      iterations: Infinity,
      easing: "ease-in-out",
    }
  );
});
