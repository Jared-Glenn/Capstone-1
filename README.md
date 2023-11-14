# qr CodeR

### Website Functions

- Connects to the qrcode-supercharged API to create new QR codes for users.
- Offer several optional customization options that can alter the QR Code, including image integration and foreground and background colors.
- Stores created QR codes by user for ease of access.

### Code Creator Inputs

Each of the given fields are available for use. If you want to adjust these fields from their default, simply input a value matching the criteria below. Otherwise, black fields will use the defaults.


#### Text

This text will be encoded into the QR Code provided. This is often a link of some sort, but can also simply be text.
(Default = None)

#### Size

This will determine the size of the file and data returned.
(Default = 400)

#### Logo URL

Input a image url to incorporate into the QR Code.
(Default = None)

#### Gradient Type

Choose from diagonal, horizontal, or vertical. This determines the direction of the gradient.
(Default = None)

#### Block Style

Choose from square, round, or dot. This determines the appearance of the internal nodes of the code.
(Default = None)

#### Gradient

You can set this to 0 to disable the gradient, as well.
(Default = 1)

#### Starting Color for Gradient

Input as a hex color code. When a gradient has been selected, the color will start at this hex code.
(Default = FF0000)

#### Ending Color for Gradient

Input as a hex color code. When a gradient has been selected, the color will end at this hex code.
(Default = 00FF00)

#### Foreground Color

        <p class="documentation-text">
            Input as a hex color code. Determines the color of the nodes for the 
            output.
        </p>
        <p class="documentation-text"><strong>(Default = FF0000) </strong></p>
        <br>

    <h4>Background Color</h4>

        <p class="documentation-text">
            Input as a hex color code. Determines the color of the space between the 
            nodes for the output.
        </p>
        <p class="documentation-text"><strong>(Default = FFFFFF) </strong></p>
        <br>

    <h4>Eye Style</h4>

        <p class="documentation-text">
            Choose between circle and square. Determines the shape of the larger exterior 
            nodes that provide a focus for the camera.
        </p>
        <p class="documentation-text"><strong>(Default = None) </strong></p>
        <br>

    <h4>Validations</h4>

        <p class="documentation-text">
            Determines how thorough you want the QR Code to be validated. This includes 
            checks on its readability, color composition, and logo selection. The more validations you 
            include, the more likely that your design will be rejected and not delivered by the API.
        </p>
        <p class="documentation-text"><strong>(Default = 0) </strong></p>
        <br>

    <h4>Logo Size</h4>

        <p class="documentation-text">
            Determines how much space the logo will occupy in the code. For simple 
            text inputs, the size of the logo may larger, but more complex URLs may struggle with 
            larger logos.
        </p>
        <p class="documentation-text"><strong>(Default = 0.22) </strong></p>
        <br>

<h2>Project Outline</h2>

<h3>Schema</h3>

    <p class="documentation-text"><strong>Users database:</strong> User (id, username, hashed password, 
        email, first_name, last_name) -> One to many</p>
    <p class="documentation-text"><strong>QR Codes database:</strong> Code (id, code text, 
        code file location, size*, logo url*, gradient type*, block style*, gradient*, starting color gradient*,
        ending color gradient*, foreground color*, background color*, eye style*, number of validations*,
        logo size*, user_id)</p>
    <p class="documentation-text">(* = Optional)</p>

<h3>Storage</h3>

    <p class="documentation-text">An initial concern for the project was the storage of the actual 
        code in a database. After some research, I determined that it would be more efficient to store 
        the file locally and store the file location in the database. This is how the system has been 
        implemented.
    </p>

<h3>Security</h3>

    <p class="documentation-text">Emails and real life names will be protected by hashed and salted 
        password generation. Likewise, individual codes are tied to individual users for security.</p>

<h3>User Flow</h3>

    <p class="documentation-text">While not signed in, users may access the documentation page (this page), the 
        registration page, and the login page. This allows potential users to understand the webapp 
        and register to use it. Current users can simply access the login page to access their own 
        pages.
    </p>

    <p class="documentation-text">The "/" or home page of the site will lead to the registration page 
        by default, unless the user is already logged in. If the user is logged in (or after logging in), 
        the user will be sent to the user home page, where personal information is available, as well as 
        all previously created QR Codes.
    </p>

    <p class="documentation-text">From this page, users may push the "Create a New Code" button to access 
        the code creation form. Once submitted (if accepted), this new code will be displayed on the user's 
        home page, as well.
    </p>


{% endblock %}















# Capstone-1 (QR Coder) - (Original Website Plan)

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
QR database: QrCodes (id, code jpg, preferences[?] user_id)

#### Issues

Generating and storing the actual QR Code, along with custom attributes could be data-intensive. That will be among the first things I investigate. Once the code is generated, how is the data delivered and how can I render it on my webpage?

#### Security

Emails and real life names will be protected by hashed and salted password generation. The actual QR Codes will likely be publically available on a gallary to inspire new creators.

#### User Flow

The home page will allow a user to create a custom QR code using the qrcode-monkey API, but also contain a link to register or login. The user will be warned that, while not signed in, all generated QR Codes will not be stored by the site.

A registration page and login page will give users access to their own personal information and a personal gallary of their created QR codes. You can also navigate back to the home page, which will now store generated QR codes under the user's user_id.

An additional page will add QR codes as they are generated by the community, mixing random QR codes onto the page, with parameters for how they were created. This page is meant to inspire creators to try a new style.



