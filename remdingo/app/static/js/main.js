function getUUID() {
    return crypto.randomUUID();
}

const getCookie = (name) => {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim().split('=');
        if (c[0] === name) {
            return c[1];
        }
    }
    return "";
}

const setCookie = (name, value, days=7) => {
    let cookie = `${name}=${encodeURIComponent(value)}`;

    if (days) {
        const expiry = new Date();
        expiry.setDate(expiry.getDate() + days);
        cookie += `; expires=${expiry.toUTCString()}`;
    }

    cookie += `; path=/`;
    //cookie += `; domain=${domain}`;
    cookie += `; secure`;

    document.cookie = cookie;
};

let customerId = getCookie('_remdingo');

if(customerId) {
    //console.log("getting cookie");
    //console.log("cookie: " + customerId);
} else {
    //console.log("setting cookie");
    setCookie('_remdingo', getUUID(), 7);
    customerId = getCookie('_remdingo');
}

$('#first_timers').hide();