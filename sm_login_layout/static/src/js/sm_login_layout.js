/**
 * Background Login Layout - runs on the login, signup and reset password pages.
 *
 * Plain browser script (no module system) so the same file works on every Odoo
 * version from 14 to 19. It reads the settings the server put on `.sm-login-bg`,
 * decides between the day and night wallpaper set from the visitor local clock,
 * and rotates the images as a slideshow when there is more than one.
 */
(function () {
    "use strict";

    function ids(value) {
        return (value || "").split(",").map(function (s) { return s.trim(); }).filter(Boolean);
    }

    function isNight(bg) {
        if (bg.dataset.nightEnabled !== "1") {
            return false;
        }
        var hour = new Date().getHours();
        var start = parseInt(bg.dataset.nightStart, 10);
        var end = parseInt(bg.dataset.nightEnd, 10);
        if (isNaN(start) || isNaN(end)) {
            return false;
        }
        // window may wrap past midnight, e.g. 19:00 to 06:00
        return start < end ? (hour >= start && hour < end) : (hour >= start || hour < end);
    }

    function wallpaperUrl(id) {
        return "/sm_login/wallpaper/" + id;
    }

    function start() {
        var bg = document.querySelector(".sm-login-bg");
        if (!bg) {
            return;
        }
        document.body.classList.add("sm-login-active");
        document.body.classList.add("sm-login-design-" + (bg.dataset.design || "1"));
        ["--sm-overlay", "--sm-overlay-op", "--sm-card-op", "--sm-blur"].forEach(function (name) {
            var value = bg.style.getPropertyValue(name);
            if (value) {
                document.body.style.setProperty(name, value);
            }
        });

        var night = ids(bg.dataset.night);
        var day = ids(bg.dataset.day);
        var chosen = isNight(bg) && night.length ? night : (day.length ? day : night);
        if (!chosen.length) {
            return; // custom login on, but no wallpaper uploaded yet
        }

        var index = 0;
        function show(i) {
            var img = new Image();
            img.onload = function () {
                document.body.style.setProperty("--sm-login-image", "url('" + wallpaperUrl(chosen[i]) + "')");
                document.body.style.setProperty("--sm-login-image-op", "1");
            };
            img.src = wallpaperUrl(chosen[i]);
        }
        show(0);

        if (chosen.length > 1) {
            var interval = Math.max(2, parseInt(bg.dataset.interval, 10) || 8) * 1000;
            setInterval(function () {
                index = (index + 1) % chosen.length;
                document.body.style.setProperty("--sm-login-image-op", "0");
                setTimeout(function () { show(index); }, 450);
            }, interval);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", start);
    } else {
        start();
    }
})();
