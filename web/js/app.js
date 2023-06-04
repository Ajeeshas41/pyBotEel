
let loading = function(func){

  return async args => {
    document.getElementById('preloader').classList.add('htmx-request')
    let res = await func(args)
    document.getElementById('preloader').classList.remove('htmx-request')
    return res
  }

}

async function D_callPYWrite (text) {
    const res = await eel.print_text(text)()
    document.getElementById("test").innerHTML = `<h1>${ res } - send to backend.`
}

const callPYWrite = loading(D_callPYWrite)