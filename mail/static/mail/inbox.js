document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-submit').addEventListener('click', submit_email)
  // By default, load the inbox
  load_mailbox('inbox');
});

function submit_email(event) {
  event.preventDefault();

  message = {
    recipients: document.querySelector('#compose-recipients').value,
    subject: document.querySelector('#compose-subject').value,
    body: document.querySelector('#compose-body').value
  }

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify(message)
  })
    .then(response => response.json())
    .then(result => {
      load_mailbox('sent');
    })
}

function compose_email(recipients='', subject='', body='') {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;
}


function update_archived(event,id) {
  const isBtnArchiving = event.target.textContent === "Archive";

  fetch('emails/' + id, {
      method: 'PUT',
      body: JSON.stringify({
        archived: isBtnArchiving
      })
    })
    .then(() => {
      load_mailbox('inbox');
      //event.target.textContent = isBtnArchiving ? "Unarchive" : "Archive";
    })
    .catch(error => console.log("Błąd:", error));
}



function create_mail_element(mail,show_archive_btn) {
  const mailDiv = document.createElement('div');
  mailDiv.classList.add('border', 'rounded', 'border-secondary', 'p-3', 'mb-2', 'shadow');
  if (mail.read)
    mailDiv.classList.add('bg-dark', 'text-light')

  const mailContent = `
    <div class="row">
      <div class="col text-left"><b>${mail.sender}</b></div>
      <div class="col text-right">${mail.timestamp}</div>
    </div>
    <div>${mail.subject}</div>
  `;

  mailDiv.innerHTML = mailContent;
  mailDiv.addEventListener('click', () => {
    fetch('emails/' + mail.id,
      {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      });
    show_email(mail,show_archive_btn=show_archive_btn);
  });

  return mailDiv;
}


function load_mailbox(mailbox) {
  fetch('emails/' + mailbox)
    .then(response => response.json())
    .then(mailList => {
      document.querySelector('#emails-view').innerHTML = '';
      console.log(mailList);
      mailList.forEach(mail => {
        const mailElement = create_mail_element(mail,show_archive_btn = !(mailbox=='sent'));
        document.querySelector('#emails-view').append(mailElement);
      });
    })

  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

}

function get_archive_button(is_archived)
{
  return  `<button id="archive-button" class="btn btn-primary mt-3">` + 
    (is_archived ? "Unarchive" : "Archive") + `</button>` ;
}

function get_reply_button()
{
  return `<button id="reply-button" class="btn btn-primary mt-3" value="abc">Reply</button>`
}

function show_email(mail,show_archive_btn) {

  document.querySelector('#emails-view').innerHTML = '';
  
  let archive_button = (show_archive_btn)? get_archive_button(mail.archived) : "";
  let reply_button = get_reply_button(mail.archived);
  const pageContent = `
    <div>
      <hr>
      <b>Subject: </b>${mail.subject}<br>
      <b>From: </b>${mail.sender}<br>
      <b>To: </b>${mail.recipients}<br>
      <b>Timestamp: </b>${mail.timestamp}<br>
       ${reply_button} ${archive_button}
      <hr>
    </div>
    <div>
      ${mail.body}
    </div>`;

  document.querySelector('#emails-view').innerHTML = pageContent;
  document.querySelector('#archive-button')?.addEventListener('click', (event)=>update_archived(event,mail.id));
  document.querySelector('#reply-button').addEventListener('click', ()=>make_reply(mail));
}

function make_reply(mail)
{
  re = mail.subject.startsWith("Re:") ? '' : 'Re: '
  compose_email(recipients=mail.sender,subject=re+mail.subject,body=`On ${mail.timestamp} ${mail.sender} wrote: \n`+mail.body+'\n');
}