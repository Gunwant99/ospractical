(function () {
    const links = [
        ["/cpu-scheduling", "CPU Scheduling"],
        ["/producer-consumer", "Producer–Consumer"],
        ["/bankers", "Banker's Algorithm"],
        ["/memory", "Memory Management"]
    ];
    const here = location.pathname.replace(/\/$/, "");
    const nav = document.createElement("nav");
    nav.className = "topnav";
    nav.innerHTML = '<a class="brand" href="/">OS Visualizer</a>' +
        links.map(([href, label]) =>
            `<a href="${href}"${href === here ? ' class="active" aria-current="page"' : ""}>${label}</a>`
        ).join("");
    document.body.prepend(nav);
})();
