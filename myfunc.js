myfunc = {};

//*********************************************************************************** */
myfunc.submit = function(){ //request can be insert or update
    var xhr = new XMLHttpRequest();
    var fdata = new FormData();
    var ops = {};
    var resfilename = "";
    var filename = "";
    
    ops[document.getElementsByName("chooseaction")[0].id] = document.getElementsByName("chooseaction")[0].checked;
    ops[document.getElementsByName("chooseaction")[1].id] = document.getElementsByName("chooseaction")[1].checked;
    

    if(ops["removepass"]==true){
        if(document.getElementById("xlsxfile").files.length == 0){
            return;
        }
        else{
            fdata.append("action","removepass");
            fdata.append("xlsxfile",document.getElementById("xlsxfile").files[0]);
        }
    }
    else if(ops["returnpass"]==true){
        if(document.getElementById("xlsxfile").files.length == 0){
            return;
        }
        if(document.getElementById("jsonfile").files.length == 0){
            return;
        }
        else{
            fdata.append("action","returnpass");
            fdata.append("xlsxfile",document.getElementById("xlsxfile").files[0]);
            fdata.append("jsonfile",document.getElementById("jsonfile").files[0]);
        }        
    }
    
    filename = document.getElementById("xlsxfile").files[0].name.toLowerCase();

    if (filename.endsWith(".xlsx")){
        resfilename = "result.xlsx"
    }
    else if (filename.endsWith(".xlsm")){
        resfilename = "result.xlsm"
    }

    xhr.open('POST',"http://localhost:"+ui.port,true)

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {   
            console.log(this.responseText)

            resobj = JSON.parse(this.responseText);

            if (resobj[0] == "Error"){
                alert(resobj[1])
            }
            else{
                if (ops["removepass"]==true){
                    myfunc.download(resfilename,resobj[0])
                    myfunc.download("passes.json",resobj[1])     
                }
                else if (ops["returnpass"]==true){
                    myfunc.download(resfilename,resobj[0])
                }
            }
        }
    }

    xhr.send(fdata);     
}


//********************************************************************************************* */
myfunc.download = function(filename, filetext){

    var a = document.createElement("a");

    document.body.appendChild(a);

    a.style = "display: none";

    a.href = 'data:application/octet-stream;base64,' + filetext;

    a.download = filename;

    a.click();

    document.body.removeChild(a);

}
