function UploadImage() {
    let input = document.getElementById("uploadImage")
    let file = input.files[0];

    let formData = new FormData();
    formData.append('file', file)

    fetch("/detect", {
        method: "POST",
        body: formData
    })
        .then(response => response.blob())
        .then(blob => {
            let url = URL.createObjectURL(blob);
            document.getElementById("resultImage").src = url;
        })
}