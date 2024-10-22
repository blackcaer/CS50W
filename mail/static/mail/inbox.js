document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-submit').addEventListener('click',submit_email)
  // By default, load the inbox
  load_mailbox('inbox');
});

function submit_email(event){
  event.preventDefault();

  message = {
    recipients: document.querySelector('#compose-recipients').value,
    subject: document.querySelector('#compose-subject').value,
    body: document.querySelector('#compose-body').value
  }
  // console.log(message);
  // console.log(JSON.stringify(message));

  fetch('/emails',{
    method: 'POST',
    body: JSON.stringify(message)
  })
  .then(response => response.json())
  .then(result => {
    //console.log(result);
    load_mailbox('sent');
  }) 
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function createMailElement(mail) {
  const mailDiv = document.createElement('div');
  mailDiv.classList.add('border', 'rounded', 'border-secondary', 'p-3', 'mb-2', 'shadow');
  if(mail.read)
    mailDiv.classList.add('bg-dark','text-light')

  const mailContent = `
    <div class="row">
      <div class="col text-left"><b>${mail.sender}</b></div>
      <div class="col text-right">${mail.timestamp}</div>
    </div>
    <div>${mail.subject}</div>
  `;

  mailDiv.innerHTML = mailContent;
  mailDiv.addEventListener('click', () => {
    fetch('emails/'+mail.id,
      {
        method: 'PUT',
        body: JSON.stringify({
          read:true
        })
      });
    show_email(mail.id);
  });
  
  return mailDiv;
}

function show_email(id)
{
  
  document.querySelector('#emails-view').innerHTML = '';
  fetch('/emails/'+id)
  .then(response => response.json())
  .then(result => {
    console.log(result);
    let mail = result;
    console.log("maail:");
    console.log(mail);
    const pageContent = `
      <div>
      <hr>
      <b>Subject: </b>${mail.subject}<br>
      <b>From: </b>${mail.sender}<br>
      <b>To: </b>${mail.recipients}<br>
      <b>Timestamp: </b>${mail.timestamp}<br>
      <hr>
      </div>
      <div>${mail.body}
      </div>
    `;

    document.querySelector('#emails-view').innerHTML = pageContent;
  })

}

function load_mailbox(mailbox) {
  fetch('emails/'+mailbox)
  .then(response => response.json())
  .then(mailList => {
    console.log(mailList);

    document.querySelector('#emails-view').innerHTML = '';
    mailList.forEach(mail => {
      const mailElement = createMailElement(mail);
      document.querySelector('#emails-view').append(mailElement);
    });
  }) 

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


}