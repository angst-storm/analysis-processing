let widgetManager = {
    init: function (id) {
        let widget = document.getElementById(id);
        widget.innerHTML = this.widgetCode;
        let form = widget.querySelector("form");
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
            }).then(res => res.json().then(this.actionWithResult));
        });
    },
    actionWithResult: function (res) {
        alert(res['parsing_result'])
    },
    widgetCode:
        '<form method="post" action="http://127.0.0.1:8000/" enctype="multipart/form-data"\n' +
        '      style="' +
        'display: flex;' +
        'flex-direction: column;' +
        'padding: 20px;' +
        'background-color: lightblue;' +
        'border: 10px solid transparent;' +
        'text-align: center;min-width: 350px;' +
        'min-height: 50px;' +
        'border-image: 10 repeating-linear-gradient(135deg,red,red 10px,transparent 10px,transparent 20px,whitesmoke 20px,whitesmoke 30px,transparent 30px,transparent 40px);">\n' +
        '    <label>PDF-файл:\n' +
        '        <input type="file" name="pdf_file" required>\n' +
        '    </label><br>\n' +
        '    <input type="submit">\n' +
        '</form>'
}