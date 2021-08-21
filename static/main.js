// Credit: https://codepen.io/t7team/pen/ZowdRN
function openTab(e, tabName) {
    let i, x, tabLinks;
    x = document.getElementsByClassName('content-tab');
    for (i = 0; i < x.length; i++) {
        x[i].style.display = 'none';
    }
    tabLinks = document.getElementsByClassName('tab');
    for (i = 0; i < x.length; i++) {
        tabLinks[i].className = tabLinks[i].className.replace(' is-active', '');
    }
    document.getElementById(tabName).style.display = 'block';
    e.className += ' is-active';
}

function submitSrcImage() {
    let srcImage = document.getElementById("srcImage");
    srcImage.click();
    srcImage.onchange = function (e) {
        let image = srcImage.files[0];
        if (image) {
            document.getElementById('showSrcImage').src = URL.createObjectURL(image);
        }

    }
}

function submitRefImage() {
    let refImage = document.getElementById("refImage");
    refImage.click();
    refImage.onchange = function (e) {
        let image = refImage.files[0];
        if (image) {
            document.getElementById('showRefImage').src = URL.createObjectURL(image);
        }

    }
}

async function StarGANv2Generate() {
    let form = new FormData();
    let y = document.getElementById('y').value;
    let seed = document.getElementById('seed').value;
    let isRef = document.getElementById("refRadio").checked;
    let mode = "latent";
    if (isRef) mode = "reference"
    let src_img = document.getElementById("srcImage").files[0];
    if (isRef) {
        let ref_img = document.getElementById("refImage").files[0];
        form.append("ref_img", ref_img, "ref_img");
    }
    form.append("model", "starganv2_afhq");
    form.append("y", y);
    form.append("seed", seed);
    form.append("mode", mode);
    form.append("src_img", src_img, "src_img");
    let res = await fetch("/api/model", {
        method: 'post',
        body: form
    });
    let data = await res.json();
    if (data.success) {
        document.getElementById('showResImage').src = "/" + data.data[0];
    } else {
        showErrorMessage(data.message);
    }
}


function showErrorMessage(message, duration = 5) {
    console.error(message);
    let e = document.getElementById('errorMessage');
    e.children[0].textContent = `Error: ${message}`;
    e.style.display = 'block';
    setTimeout(() => {
        e.style.display = 'none';
    }, duration * 1000);
}