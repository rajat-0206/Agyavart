var hide = 'none',show = 'block';
class Snackbar{
    id = 'snackBar';
    textId = 'snackText';
    buttonId = 'snackButton';
    normalSnack = 'snack-normal';
    warningSnack = 'snack-warning';
    errorSnack = 'snack-error';
    showSnack = 'snack-show';
    hideSnack = 'snack-hide';
    //You can modify the following values for color codes of the three snackbar backgrounds.
    normalBack = '#216bd3';
    warnBack = '#aa8800';
    errBack = '#c41010';

    constructor(){
        this.bar = document.getElementById(this.id);
        this.text = document.getElementById(this.textId);
        this.button = document.getElementById(this.buttonId);
    }
}

/**
 * Call this function whenever you want to display a snackbar message, customizing with following params.
 * @param {*} text The text to be displayed as snackbar message.
 * @param {*} hasAction If the snackbar has an associated action button, set this as true. Default is false.
 * @param {*} actionText Set text on action button, if hasAction is true.
 * @param {*} isNormal If set as true (default), a normal style snackbar UI will be created. Error style UI will be created if false.
 * @param {*} isWarning If set as true, a warning style (moderate error) snackbar UI will be created. Default is false.
 */
function showSnackBar(text = String(),hasAction = false,actionText = String(),isNormal = true,isWarning = false){
    var snack = new Snackbar();
    snack.text.textContent = text;
    if(hasAction){
        snack.button.textContent = actionText;
        snack.button.style.display = show;
    } else {
        snack.button.style.display = hide;
    }
    if(isNormal){
        replaceClasses(snack.bar,Array(snack.warningSnack,snack.normalSnack,snack.errorSnack),snack.normalSnack);
        snack.bar.style.backgroundColor = snack.normalBack;
    } else {
        if(isWarning){
            replaceClasses(snack.bar,Array(snack.warningSnack,snack.normalSnack,snack.errorSnack),snack.warningSnack);
            snack.bar.style.backgroundColor = snack.warnBack;
        } else {
            replaceClasses(snack.bar,Array(snack.warningSnack,snack.normalSnack,snack.errorSnack),snack.errorSnack);
            snack.bar.style.backgroundColor = snack.errBack;
        }


    }
    snack.bar.classList.replace(snack.hideSnack,snack.showSnack);
    snack.bar.style.display = show;
    setTimeout(function(){
        hideSnackBar();
    },3000);
}

function replaceClasses(element,remove,set){
    for(var k in remove){
        element.classList.remove(k);
    }
    element.classList.add(set);
}

/**
 * This method hides the current snackbar upon call.
 */
function hideSnackBar(){
    var snack = new Snackbar();
    replaceClasses(snack.bar,Array(snack.warningSnack,snack.normalSnack,snack.errorSnack),snack.normalSnack);
    snack.bar.classList.replace(snack.showSnack,snack.hideSnack);
    snack.bar.style.display = hide;
}