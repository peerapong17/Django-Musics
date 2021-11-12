const button = document.getElementById("button");
const selectedPlaylists = document.getElementsByName("selectedPlaylists")
let songId = 0


function showModal(id) {
    songId = id
    fetch("/playlists/add-song/" + songId, {
        method: "GET",
    })
        .then((res) => res.json())
        .then((res) => {
            console.log(res.length > 0)
            console.log(res)
            console.log(selectedPlaylists)
            if (res.length > 0) {
                for (let i = 0; i < selectedPlaylists.length; i++) {
                    selectedPlaylists[i].checked = false
                    for (let u = 0; u < res.length; u++) {
                        if (selectedPlaylists[i].id == res[u].pk) {
                            selectedPlaylists[i].checked = true
                        }
                    }
                }
            } else {
                console.log(selectedPlaylists)
                for (let i = 0; i < selectedPlaylists.length; i++) {
                    selectedPlaylists[i].checked = false
                }
            }
        })
}

button.addEventListener("click", () => {
    let dataList = []
    for (let playlist of selectedPlaylists) {
        if (playlist.checked === true) {
            dataList.push(playlist.value)
        }
    }

    const fd = new FormData();
    fd.append("selectedPlaylists", dataList);

    fetch("/playlists/add-song/" + songId, {
        method: "POST",
        body: fd,
        headers: {'X-CSRFToken': '{{ csrf_token }}'}
    })
})