$(document).ready(function() {
    $('.submit').click(function (event) {
        event.preventDefault()

        var name= $('.name').val()
        var email= $('.email').val()
        var comments= $('.comments').val()
        var statuselm=$('.status')
        statuselm.empty()

        if(name.length>2){
            statuselm.append('<div>name is valid</div>')
        } else 
        {
            event.preventDefault()
            statuselm.append('<div>name is invalid </div>')
        }

        if(email.length>5 && email.includes('@') && email.includes('.')){
            statuselm.append('<div>email is valid</div>')
        } else 
        {
            event.preventDefault()
            statuselm.append('<div>email is invalid </div>')
        }
        if(comments.length>20){
            statuselm.append('<div>comments are  valid</div>')
        } else 
        {
            event.preventDefault()
            statuselm.append('<div>comments are invalid </div>')
        }
    })
})