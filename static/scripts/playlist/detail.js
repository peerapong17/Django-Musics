$(function () {
    $('.dropdown-filter').click(function () {
        let value = $(this).attr("data-filter")
        if (value == "all") {
            $('.filter').fadeIn(300)
        } else {
            $('.filter').not('.' + value).fadeOut(300)
            $('.filter').filter('.' + value).fadeIn(300)
        }
    })
})

let songSection = document.querySelector(".song-section")

const deleteSong = (playlistId, songId) => {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            let url = `http://127.0.0.1:8000/playlists/playlist/${playlistId}/delete/${songId}`
            fetch(url)
                .then(res => res.json())
                .then(res => {
                        for (let i = 0; i < songSection.children.length; i++) {
                            if (songId == songSection.children[i].id) {
                                songSection.children[i].remove()
                            }
                        }
                        Swal.fire(
                            'Deleted!',
                            `${res}.`,
                            'success'
                        )
                    }
                )
                .catch(err => {
                    console.log(err)
                })
        }
    })
}