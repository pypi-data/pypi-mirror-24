webpackJsonp([15],{423:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={name:"HomeStepper",data:function(){return{current_step:0,starting_address:"",destination:"",starting_address_obj:{},destination_obj:{},dateStartPicker:null,dateStartPickerMenu:!1,dateEndPicker:null,dateEndPickerMenu:!1,timeStartPicer:null,timeStartPicerMenu:!1,timeEndPicer:null,timeEndPicerMenu:!1,retrieving_dialog:!1}},props:{traffic_data_received:{type:Boolean}},methods:{select_routes:function(){this.$emit("HomeStepper_select_routes",this.starting_address_obj,this.destination_obj)},select_time:function(){this.$emit("HomeStepper_select_time",this.dateStartPicker,this.dateEndPicker,this.timeStartPicer,this.timeEndPicer)},finished_querying_data:function(){this.retrieving_dialog=!1}},mounted:function(){var t=this,e=document.getElementById("starting_address"),a=new google.maps.places.Autocomplete(e);a.addListener("place_changed",function(){var e=a.getPlace();t.starting_address_obj={lat:e.geometry.location.lat(),lng:e.geometry.location.lng()}});var i=document.getElementById("destination"),r=new google.maps.places.Autocomplete(i);r.addListener("place_changed",function(){var e=r.getPlace();t.destination_obj={lat:e.geometry.location.lat(),lng:e.geometry.location.lng()}})}}},438:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-flex",{attrs:{xs12:"xs12",md6:"md6"}},[a("v-stepper",{attrs:{vertical:"vertical"},model:{value:t.current_step,callback:function(e){t.current_step=e},expression:"current_step"}},[a("v-stepper-step",{attrs:{step:"1",complete:t.current_step>1,editable:"editable"}},[t._v("Introduction")]),a("v-stepper-content",{attrs:{step:"1"}},[a("div",{staticClass:"mb-5"},[t._v(" StreetTraffic package enables you to visualzie the trafffic pattern on a selected route. \nAlthough we hope to support more geographical area, currently we only have data on Atlanta City.")]),a("v-btn",{attrs:{primary:"primary",light:"light"},nativeOn:{click:function(e){t.current_step=2}}},[t._v("Continue")])],1),a("v-stepper-step",{attrs:{step:"2",complete:t.current_step>2,editable:"editable"}},[t._v("Select a desired route")]),a("v-stepper-content",{attrs:{step:"2"}},[a("div",{staticClass:"mb-5"},[t._v("Simply pick a starting address and destination"),a("br"),a("br"),a("v-text-field",{staticClass:"input-group--focused",attrs:{label:"Starting Address",id:"starting_address"},model:{value:t.starting_address,callback:function(e){t.starting_address=e},expression:"starting_address"}}),a("v-text-field",{staticClass:"input-group--focused",attrs:{label:"Destination",id:"destination"},model:{value:t.destination,callback:function(e){t.destination=e},expression:"destination"}})],1),a("v-btn",{attrs:{primary:"primary",light:"light"},nativeOn:{click:function(e){t.current_step=3,t.select_routes()}}},[t._v("Select Them")])],1),a("v-stepper-step",{attrs:{step:"3",complete:t.current_step>3,editable:"editable"}},[t._v("Select a time interval")]),a("v-stepper-content",{attrs:{step:"3"}},[a("div",{staticClass:"mb-5"},[t._v("What is the time interval of the day that intrigues/annoys you the most? For example, you could choose the rush hours from 8:00 to 10:00"),a("br"),a("v-menu",{attrs:{lazy:"lazy","close-on-content-click":!1,"offset-y":"offset-y","nudge-left":40},model:{value:t.timeStartPicerMenu,callback:function(e){t.timeStartPicerMenu=e},expression:"timeStartPicerMenu"}},[a("v-text-field",{attrs:{label:"Start Time","prepend-icon":"access_time",readonly:"readonly"},slot:"activator",model:{value:t.timeStartPicer,callback:function(e){t.timeStartPicer=e},expression:"timeStartPicer"}}),a("v-time-picker",{attrs:{autosave:"autosave",format:"24hr"},model:{value:t.timeStartPicer,callback:function(e){t.timeStartPicer=e},expression:"timeStartPicer"}})],1),a("v-menu",{attrs:{lazy:"lazy","close-on-content-click":!1,"offset-y":"offset-y","nudge-left":40},model:{value:t.timeEndPicerMenu,callback:function(e){t.timeEndPicerMenu=e},expression:"timeEndPicerMenu"}},[a("v-text-field",{attrs:{label:"End Time","prepend-icon":"access_time",readonly:"readonly"},slot:"activator",model:{value:t.timeEndPicer,callback:function(e){t.timeEndPicer=e},expression:"timeEndPicer"}}),a("v-time-picker",{attrs:{autosave:"autosave",format:"24hr"},model:{value:t.timeEndPicer,callback:function(e){t.timeEndPicer=e},expression:"timeEndPicer"}})],1)],1),a("v-btn",{attrs:{primary:"primary",light:"light"},nativeOn:{click:function(e){t.current_step=4}}},[t._v("Continue")])],1),a("v-stepper-step",{attrs:{step:"4",complete:t.current_step>3,editable:"editable"}},[t._v("Choose a date interval")]),a("v-stepper-content",{attrs:{step:"4"}},[a("div",{staticClass:"mb-5"},[t._v("Now that you have selected the time interval of day, you can query the that interval for multiple dates. Pick a start date and an end data."),a("br"),a("v-menu",{attrs:{lazy:"lazy","close-on-content-click":!1,"offset-y":"offset-y","full-width":"full-width","nudge-left":40,"max-width":"290px"},model:{value:t.dateStartPickerMenu,callback:function(e){t.dateStartPickerMenu=e},expression:"dateStartPickerMenu"}},[a("v-text-field",{attrs:{label:"Start Date","prepend-icon":"event",readonly:"readonly"},slot:"activator",model:{value:t.dateStartPicker,callback:function(e){t.dateStartPicker=e},expression:"dateStartPicker"}}),a("v-date-picker",{attrs:{"no-title":"no-title",scrollable:"scrollable",autosave:"autosave"},model:{value:t.dateStartPicker,callback:function(e){t.dateStartPicker=e},expression:"dateStartPicker"}})],1),a("v-menu",{attrs:{lazy:"lazy","close-on-content-click":!1,"offset-y":"offset-y","full-width":"full-width","nudge-left":40,"max-width":"290px"},model:{value:t.dateEndPickerMenu,callback:function(e){t.dateEndPickerMenu=e},expression:"dateEndPickerMenu"}},[a("v-text-field",{attrs:{label:"End Date","prepend-icon":"event",readonly:"readonly"},slot:"activator",model:{value:t.dateEndPicker,callback:function(e){t.dateEndPicker=e},expression:"dateEndPicker"}}),a("v-date-picker",{attrs:{"no-title":"no-title",scrollable:"scrollable",autosave:"autosave"},model:{value:t.dateEndPicker,callback:function(e){t.dateEndPicker=e},expression:"dateEndPicker"}})],1)],1),a("v-dialog",{attrs:{persistent:"persistent"},model:{value:t.retrieving_dialog,callback:function(e){t.retrieving_dialog=e},expression:"retrieving_dialog"}},[a("v-btn",{attrs:{primary:"primary",light:"light"},nativeOn:{click:function(e){t.current_step=5,t.select_time()}},slot:"activator"},[t._v("Query Data")]),a("v-card",[a("v-card-row",[a("v-card-title",[t._v("Retrieving data from the server")])],1),a("v-card-row",[a("v-card-text",[t._v("Please be patient :)")])],1)],1)],1)],1),a("v-stepper-step",{attrs:{step:"5"}},[t._v("View setup instructions")]),a("v-stepper-content",{attrs:{step:"5"}},[a("div",{staticClass:"mb-5"},[t._v("Great! Now you have query your first data, if you want to try a different time range, hit the try again button.")]),a("v-btn",{attrs:{primary:"primary",light:"light"},nativeOn:{click:function(e){t.current_step=3}}},[t._v("Try Again")])],1)],1)],1)},staticRenderFns:[]}},73:function(t,e,a){var i=a(8)(a(423),a(438),null,null,null);t.exports=i.exports}});
//# sourceMappingURL=15.3566a45bf8d06d4fe26e.js.map