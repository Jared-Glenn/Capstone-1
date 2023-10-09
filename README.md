# Capstone-1 (QR Coder)

### Website Goals

- Create a site that connects to the qrcode-monkey API to create new QR codes for users.
- Store QR codes by user for ease of access.
- Create gallaries of styles already created on QR Coder.

### Expected Users and Data

I anticipate that QR Coder will be used by people in marketing or public relations, as QR Codes most often are used for those purposes - especially when given eye-catching graphics. My site will mostly generate its own data from users, relying on qrcode-monkey only for generating the QR codes that the users will request. QR Coder will record a username and password, along with an email and the user's first and last name. It will also store all "saved" QR codes created by that user for future use. This data might be used to store setting for future QR codes, as well.


### Project Outline

#### Schema

Primary database: Users (id, username, hashed password, email, first_name, last_name)
-> One to many
QR database: QrCodes (id, code, user_id)

#### Issues

Generating and storing the actual QR Code, along with custom attributes could be data-intensive. That will be among the first things I investigate. Once the code is generated, how is the data delivered and how can I render it on my webpage?

#### Security

Emails and real life names will be protected by hashed and salted password generation. The actual QR Codes will likely be publically available on a gallary to inspire new creators.

#### User Flow

The home page will allow a user to create a custom QR code using the qrcode-monkey API, but also contain a link to register or login. The user will be warned that, while not signed in, all generated QR Codes will not be stored by the site.

A registration page and login page will give users access to their own personal information and a personal gallary of their created QR codes. You can also navigate back to the home page, which will now store generated QR codes under the user's user_id.

An additional page will add QR codes as they are generated by the community, mixing random QR codes onto the page, with parameters for how they were created. This page is meant to inspire creators to try a new style.


