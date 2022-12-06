// Initializing the Category List
let categoryList = []

// Initializing the Initial Loading Button
let initialLoader = document.querySelector('.initial_loader');

// Initializing the main card
let aviraFashions = document.querySelector('.avira_fashions');

// Initializing 36Inch Width Chip
let _36InchChipCheckbox = document.getElementById("36_chip_checkbox");
let _36InchChip = document.getElementById("36_chip");

// Initializing 58Inch Width Chip
let _58InchChipCheckbox = document.getElementById("58_chip_checkbox");
let _58InchChip = document.getElementById("58_chip");

// Initializing the length input field
let lengthInput = document.querySelector(".length_input");

// Initializing the select category container
let selectCategoryContainer = document.querySelector(".select_category_container");

// Initializing the select category button
let selectCategoryButton = document.querySelector(".select_category_button");

// Initializing the Category List Search Input
let categoryListSearchInput = document.querySelector(".category_list_search_input");

// Initializing the Category List Items container
let categoryListItemsContainer = document.querySelector(".category_list_items");

// Initializing an array to store all the Category Items Nodes
let categoryItems = document.querySelectorAll(".category_item");

// Initializing the length input field
let clientPhoneNumberInput = document.querySelector(".client_phone_number_input");

// Initializing the generate button
let generateReadyStockButton = document.querySelector(".generate_ready_stock_button");

// Initializing the rename files button
let renameFilesButton = document.querySelector(".rename_files_button");

// Initializing the Snack Bar to show any kind of errors
let snackBar = document.querySelector(".snack_bar");

// Initializing a dictionary to store selected filters
let filters = {
    // "sheetsSelected": [],
    "width": null,
    "length": null,
    "category": [],
    "clientPhoneNumber": null
}

eel.expose(handleErrorsAndSuccess)
function handleErrorsAndSuccess(message) {
    console.log(`Python Message Received! ${message}`);
    stopLoading(message);

    // Adding a message to the SnackBar
    snackBar.innerHTML = message;

    // Displaying the SnackBar
    snackBar.classList.add("show");
    
    // Hiding the SnackBar
    setTimeout(function () { 
        snackBar.classList.remove("show");
    }, 5000);
}

function categoryItemSelect(categoryItem) {
    categoryItem.classList.toggle("checked");
    
    let checked = document.querySelectorAll(".checked"),
    btnText = document.querySelector(".btn-text")
    
    if (categoryItem.classList.contains("checked")) {
        // console.log(`${categoryItem.lastChild.innerHTML} Added`);
        filters["category"].push(categoryItem.lastChild.innerText);
    } else {
        // console.log(`${categoryItem.lastChild.innerHTML} Removed`);
        filters["category"].splice(filters["category"].indexOf(categoryItem.lastChild.innerText), 1);
    }
    
    if (checked && filters["category"].length > 0) {
        btnText.innerText = `${filters["category"].length} Selected`;
    } else {
        btnText.innerText = "Select Category";
    }

    console.log(filters["category"]);
}

function stopInitialLoading() {
    setTimeout(() => {
        initialLoader.style.display = "none";
        aviraFashions.style.visibility = "visible";
    }, 1000);
}


function addCategory() {
    // console.log("addCategory function called!");
    eel.initialize_and_get_categories()((category_list) => {
        categoryList = category_list;
        categoryListItemsContainer.innerHTML = "";
        categoryList.forEach(categoryListItem => {
                let li = 
                `<li class="category_item" onclick="categoryItemSelect(this)"><span class="checkbox"><i class="fa-solid fa-check check-icon"></i></span><span class="category_item-text">${categoryListItem}</span></li>`;
                categoryListItemsContainer.insertAdjacentHTML("beforeend", li);
        });
        stopInitialLoading();
    })
}

addCategory();

_36InchChipCheckbox.addEventListener("click", () => {
    if (_36InchChipCheckbox.checked == true){
        if (_58InchChipCheckbox.checked == true) {
            _58InchChipCheckbox.checked = false;
            _58InchChip.style.background = "#FFFFFF";
        }
        _36InchChip.style.background = "rgba(120, 212, 179, 0.4)";
        filters["width"] = _36InchChipCheckbox.value;
    } else {
        filters["width"] = null;
    }
});

_58InchChipCheckbox.addEventListener("click", () => {
    if (_58InchChipCheckbox.checked == true){
        if (_36InchChipCheckbox.checked == true) {
            _36InchChipCheckbox.checked = false;
            _36InchChip.style.background = "#FFFFFF";
        }
        _58InchChip.style.background = "rgba(166, 120, 212, 0.4)";
        filters["width"] = _58InchChipCheckbox.value;
    } else {
        filters["width"] = null;
    }
});

selectCategoryButton.addEventListener("click", () => {
    selectCategoryContainer.classList.toggle("active");
});

categoryListSearchInput.addEventListener("keyup", () => {
    let arr = [];
    let searchWord = categoryListSearchInput.value.toUpperCase();
    arr = categoryList.filter(data => {
        // console.log(data.toUpperCase().startsWith(searchWord));
        return data.toUpperCase().includes(searchWord);
    }).map(data => {
        if (filters["category"].indexOf(data) !== -1)
            return `<li class="category_item checked" onclick="categoryItemSelect(this)"><span class="checkbox"><i class="fa-solid fa-check check-icon"></i></span><span class="category_item-text">${data}</span></li>`;
        else
            return `<li class="category_item" onclick="categoryItemSelect(this)"><span class="checkbox"><i class="fa-solid fa-check check-icon"></i></span><span class="category_item-text">${data}</span></li>`;
    }).join("");
    categoryListItemsContainer.innerHTML = arr ? arr : `<p style="margin: 0; margin-top: 10px; font-family: poppins;">Category not found</p>`;
});

generateReadyStockButton.addEventListener("click", () => {
    generateReadyStockButton.style.boxShadow = "none";
    generateReadyStockButton.style.background = "#0078E7";
    generateReadyStockButton.firstElementChild.style.display = "none";
    generateReadyStockButton.lastElementChild.style.display = "block";
    
    filters["length"] = parseFloat(lengthInput.value);
    console.log(clientPhoneNumberInput.value);
    if (clientPhoneNumberInput.value != "")
        filters["clientPhoneNumber"] = "+91" + clientPhoneNumberInput.value;
    else
        filters["clientPhoneNumber"] = null;
    
    console.log(filters);
    sendFilters();
});

renameFilesButton.addEventListener("click", () => {
    renameFilesButton.style.boxShadow = "none";
    renameFilesButton.style.background = "#0078E7";
    renameFilesButton.firstElementChild.style.display = "none";
    renameFilesButton.lastElementChild.style.display = "block";
    renameFiles();
});

function stopLoading() {
    setTimeout(() => {
        generateReadyStockButton.style.boxShadow = "0px 12px 22px rgba(0, 0, 0, 0.26)";
        generateReadyStockButton.style.background = "#5EB1FD";
        generateReadyStockButton.firstElementChild.innerHTML = "Generate Ready Stock";
        generateReadyStockButton.firstElementChild.style.display = "block";
        generateReadyStockButton.lastElementChild.style.display = "none";
    }, 1000);
}

// Calls the renameFiles function written on python side
function renameFiles() {
    eel.rename_files()(() => {
        setTimeout(() => {
            renameFilesButton.style.boxShadow = "0px 12px 22px rgba(0, 0, 0, 0.26)";
            renameFilesButton.style.background = "#5EB1FD";
            renameFilesButton.firstElementChild.innerHTML = "Rename Files";
            renameFilesButton.firstElementChild.style.display = "block";
            renameFilesButton.lastElementChild.style.display = "none";
        }, 1000);
    });
}

// Calls the exchange_filters function written on python side
function sendFilters() {
    eel.exchange_filters(filters)((message) => {
        console.log(message);
        stopLoading();
    });
}