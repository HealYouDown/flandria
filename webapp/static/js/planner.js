var skills = [];
var g_Level = 1;
var g_ClassIndex = 0;
var pointsUsed = 0;
var pointsLeft = 0;
var isMobile = false;

if (/Mobi|Android/i.test(navigator.userAgent)) {
    isMobile = true;
}

const debug = true;

function updateNextLevelColorWithInstace(instance) {
    // Hacky way to change color of level if level is not reached
    // Other ways do not work because of delay (element is not there yet)
    let skill = getSkillObject($(instance.reference).parent().attr("id"));
    if (g_Level < skill.requiredLevel) {
        $('head').append('<style type="text/css">.next-level {color: red;}</style>');
    }
    else {
        $('head').append('<style type="text/css">.next-level {color: inherit;}</style>');
    }
}

function updateNextLevelColorWithSkillId(skillId) {
    let skill = getSkillObject(skillId);
    if (g_Level < skill.requiredLevel) {
        $('head').append('<style type="text/css">.next-level {color: red;}</style>');
    }
    else {
        $('head').append('<style type="text/css">.next-level {color: inherit;}</style>');
    }
}

class Skill {
    constructor(skillId, maxLevel, reliesOn) {
        this.skillId = skillId;
        this.baseSkillId = skillId.slice(0, -2);
        this.maxLevel = maxLevel;
        this.reliesOn = reliesOn;

        this.currentLevel = 0;
        this._allowed = false;
        this._skilled = false;
        
        this.tooltip = tippy(document.getElementById(this.skillId).children[1]);
        this.tooltip.set({
            arrow: true,
            animation: 'scale',
            hideOnClick: false,
            interactive: true,
            placement: "right",
            delay: 250,
            boundary: 'window',
            onShow: updateNextLevelColorWithInstace,
          })
    }

    updateSkillDescription() {
        let desc = `
        <div class="skill-description-header">
            <span class="skill-name">${this.name}</span>
            <span class="skill-level">${this.level}/${this.maxLevel}</span>
        </div>
        <div class="skill-description-sub-header">
            <span class="skill-sub">${this.requiredClass}</span>
        </div>
        `
        if (this.level > 0) {
            // Add current level description
            desc += `
            <hr class="skill-description-divider">
            <div class="skill-description">
                <div class="skill-data-list">
                    <span class="key">Req. Level: </span>
                    <span class="value">${this.currentSkillDescription["required_level"]}</span>
                </div>
                <div class="skill-data-list">
                    <span class="key">MP: </span>
                    <span class="value">${this.currentSkillDescription["mana_consumption"]}</span>
                </div>
                <div class="skill-data-list">
                    <span class="key">Cooldown: </span>
                    <span class="value">${this.currentSkillDescription["cooldown"]/1000}s</span>
                </div>
                <span>${this.currentSkillDescription["description"]}</span>
            </div>
            `;
        }
        if (this.level != this.maxLevel) {
            // Next level description
            desc += `
            <hr class="skill-description-divider">
            <span class="next-level-header">Next Level (${this.level+1}):</span>
            <div class="skill-description">
                <div class="skill-data-list">
                    <span class="key">Req. Level: </span>
                    <span class="value next-level">${this.nextSkillDescription["required_level"]}</span>
                </div>
                <div class="skill-data-list">
                    <span class="key">MP: </span>
                    <span class="value">${this.nextSkillDescription["mana_consumption"]}</span>
                </div>
                <div class="skill-data-list">
                    <span class="key">Cooldown: </span>
                    <span class="value">${this.nextSkillDescription["cooldown"]/1000}s</span>
                </div>
                <span>${this.nextSkillDescription["description"]}</span>
            </div>
            `;
        }

        this.tooltip.setContent(desc);
    }

    get currentSkillId() {
        let id = this.baseSkillId;
        if (this.level < 10) {
            id += "0" + this.level;
        }
        else if (this.level >= 10 ) {
            id += this.level;
        }
        return id;   
    }

    get nextSkillId() {
        let id = this.baseSkillId;
        let level = this.level + 1;

        if (level < 10) {
            id += "0" + level;
        }
        else if (level >= 10 ) {
            id += level;
        }
        return id;   
    }

    get skilled() {
        return this._skilled;
    }

    set skilled(bool) {
        this._skilled = bool
        if (bool) {
            $(`#${this.skillId} div.skill-icon-effect-wrapper`).addClass("skilled")
        }
        else {
            $(`#${this.skillId} div.skill-icon-effect-wrapper`).removeClass("skilled")
        }
    }

    get allowed() {
        return this._allowed;
    }

    set allowed(bool) {
        this._allowed = bool;
        if (bool) {
            $(`#${this.skillId} div.skill-icon-effect-wrapper`).addClass("allowed")
        }
        else {
            $(`#${this.skillId} div.skill-icon-effect-wrapper`).removeClass("allowed")
        }
    }

    get currentSkillDescription() {
        return skillsDescriptionData[this.currentSkillId];
    }

    get nextSkillDescription() {
        return skillsDescriptionData[this.nextSkillId];
    }

    get requiredLevel() {
        if (this.nextSkillDescription != undefined)
            return parseInt(this.nextSkillDescription["required_level"]);
        return -1;
    }

    get currentRequiredLevel() {
        return parseInt(this.currentSkillDescription["required_level"]);
    }
    
    get name() {
        return this.currentSkillDescription["name"];
    }

    get requiredClass() {
        return this.currentSkillDescription["class_land"];
    }

    get level() {
        return parseInt(this.currentLevel);
    }

    set level(lv) {
        this.currentLevel = lv;
        updateNextLevelColorWithSkillId(this.skillId);
    }

    updateIsAllowed() {
        this.allowed = false;

        let selectedClass = $('#classSelect option').eq(g_ClassIndex).val();

        if (!["Noble", "Mercenary", "Explorer", "Saint", "No Class", "Base Ship"].includes(this.requiredClass)) {
            if (this.requiredClass.toLowerCase().indexOf(selectedClass) == -1) {
                if (debug) 
                    console.log("Does not have needed Class -> not allowed:", this.name)
                return;
            }
        }


        if (this.reliesOn != null) {
            if (this.reliesOn.length == 1) {
                let childSkill = getSkillObject(this.reliesOn[0]);
                if (!childSkill.skilled) {
                    if (debug)
                        console.log("Parent Skill", childSkill.name, "not skilled -> not allowed:", this.name)
                    return;
                }
            }
            else if (this.reliesOn.length == 2) {
                let childSkill_1 = getSkillObject(this.reliesOn[0]);
                if (!childSkill_1.skilled) {
                    if (debug)
                        console.log("Parent Skill", childSkill_1.name, "not skilled -> not allowed:", this.name)
                    return;
                }

                let childSkill_2 = getSkillObject(this.reliesOn[1]);
                if (!childSkill_2.skilled) {
                    if (debug)
                        console.log("Parent Skill", childSkill_2.name, "not skilled -> not allowed:", this.name)
                    return;
                }
            }
        }

        if (this.currentRequiredLevel > g_Level) {
            if (debug)
                console.log("Skill:", this.name, "-> required level is wrong:", this.requiredLevel);
            return;
        }

        if (debug) 
            console.log("Allow skill", this.name)
        this.allowed = true;
    }

    _setLevel(level) {
        if (level > 0) {
            this.level = level;
            $(`#${this.skillId} span.level`).html(level);
            this.skilled = true;
            updateAllowedSkills();
        }
        else if (level == 0) {
            this.level = level;
            $(`#${this.skillId} span.level`).html(level);
            this.skilled = false;
        }
        this.updateSkillDescription();
    }

    levelUp() {
        if (!(pointsLeft >= 1)) {
            return
        }

        if (this.level == 0) {
            // Skill is now skilled -> update child skills
            this._setLevel(1)
            updateAllowedSkills();
        }
        else if (this.level < this.maxLevel) {
            this._setLevel(this.level + 1)
        }
    }

    levelDown() {
        if (this.level == 1) {
            // Skill is now lv 0 -> reset parent skills
            this._setLevel(0)
            $(getChildSkills(this.skillId)).each(function(index, skillId) {
                let childSkill = getSkillObject(skillId);
                childSkill._setLevel(1);
                childSkill.levelDown();
            });
            updateAllowedSkills();
        }
        else if (this.level > 1) {
            this._setLevel(this.level - 1)
        }
    }
}

function updateHash() {
    // Hash: Level:Class.<Skills>.<Stat Points>

    // Level and Class
    let hash = "";

    let selectedLevel = $("#levelSelect").val();
    let selectedClassIndex = $("#classSelect").prop('selectedIndex');

    hash += `${selectedLevel}:${selectedClassIndex}.`;
    
    // Skills 
    $(skills).each(function (index, skill) {
        if (index == 0) { // No : in front
            hash += `${skill.level}`;
        }
        else {
            hash += `:${skill.level}`
        }
    });
    
    // Stat points
    // 1: Strength | 2: Dexterity | 3. Constituion | 4. Intelligence | 5. Wisdome | 6. Will
    hash += `.0:0:0:0:0:0`

    history.replaceState(undefined, undefined, `#${hash}`)
}

function updateObjectsBasedOnHash() {
    let level = getFromHash({level: true})
    $("#levelSelect").val(level);
    g_Level = level;

    let selectedClassIndex = getFromHash({classIndex: true})
    $('#classSelect option').eq(selectedClassIndex).prop('selected', true);
    g_ClassIndex = selectedClassIndex;

    let indexToLevel = getFromHash({skills: true})
    $(skills).each(function(index, skill) {
        skill._setLevel(indexToLevel[index]);
    });
}

function updateAllowedSkills() {
    if (debug)
        console.log("Updating allowed skills")
    $(skills).each(function(index, skill) {
        skill.updateIsAllowed();
    })
}

function getFromHash(options) {
    // level=false, classIndex=false, skills=false, skillId=null
    let hash = window.location.hash.replace("#", "");
    let hashParts = hash.split(".");

    if (options.level || options.classIndex) {
        let levelPart = hashParts[0];
        let levelHashParts = levelPart.split(":");
        // Array[0] = Level, Array[1] = Selected Class Index
        if (options.level == true) {
            return levelHashParts[0];
        }
        else if (options.classIndex == true) {
            return levelHashParts[1]
        }
    }
    else if (options.skills == true) {
        let skillPart = hashParts[1];
        let indexToLevel = {}

        $(skillPart.split(":")).each(function (index, skillLevel) {
            indexToLevel[index] = skillLevel;
        })
        return indexToLevel;
    }
}

function getSkillObject(skillId) {
    let toReturn;
    $(skills).each(function (index, skill) {
        if (skill.skillId == skillId) {
            toReturn = skill;
            return false;
        }
    })
    return toReturn;
}

function getChildSkills(skillId, parentSkills=[]) {
    $(skills).each(function(index, skill) {
        
        if (skill.reliesOn != null && skill.reliesOn.includes(skillId)) {
            // Filter out duplicates
            if (!parentSkills.includes(skill.skillId)) { 
                parentSkills.push(skill.skillId);
                return getChildSkills(skillId, parentSkills);
            }
        }
    })

    return parentSkills;
}

function onLevelChange() {
    let newLevel = parseInt($(this).val());

    if (newLevel < g_Level) {
        // Level was changed to a lower value -> reset
        g_Level = newLevel;
        reset();
        onClassChange();
        updatePoints();
        return;
    }

    g_Level = newLevel;
    updatePoints();
    updateHash();
    updateAllowedSkills();
}

function onClassChange() {
    let newIndex = $("#classSelect").prop('selectedIndex');

    if (newIndex != 0) {
        if (!isShipSkilltree) {
            if (!(g_Level >= 40)) {
                $('#classSelect option').eq(0).prop('selected', true);
                return;
            }
        }
    }

    g_ClassIndex = newIndex;
    
    updateAllowedSkills();
    resetCCSkills()
    updateHash()
    updatePoints();
}

function onSkillClick(event) {
    let skillId = $(this).attr("id");
    let skill = getSkillObject(skillId);

    if (event.which == 1) {
        if (skill.allowed) {
            if (event.shiftKey) {
                for (i=0; i<skill.maxLevel; i++) {
                    if (skill.level == skill.maxLevel) {
                        return false;
                    }
                    else if (skill.requiredLevel <= g_Level) {
                        skill.levelUp();
                        updatePoints(); // We have to update points every loop
                    }
                }
            }
            else {
                skill.levelUp();
            }
        }
    }
    else if (event.which == 3) {
        if (skill.skilled) {
            if (event.shiftKey) {
                skill._setLevel(1);
                skill.levelDown();
            }
            else {
                skill.levelDown();
            }
        }
    }
    updatePoints();
    updateHash();
}

function mobileLevelUp() {
    let skillId = $(this).parent().attr("id");
    let skill = getSkillObject(skillId);

    if (skill.allowed) {
        skill.levelUp();
    }
    updatePoints();
    updateHash();
}

function mobileLevelDown() {
    let skillId = $(this).parent().attr("id");
    let skill = getSkillObject(skillId);

    if (skill.allowed) {
        skill.levelDown();
    }
    updatePoints();
    updateHash();
}

function updatePoints() {
    let maxPointsToSpend = 0;
    if (g_Level <= 100)
        maxPointsToSpend = g_Level;
    else if (g_Level <= 104)
        maxPointsToSpend = 100;
    else if (g_Level == 105)
        maxPointsToSpend = 101;

    let _pointsUsed = 0;
    $(skills).each(function(index, skill) {
        _pointsUsed += skill.level;
    });

    pointsLeft = maxPointsToSpend - _pointsUsed;
    pointsUsed = _pointsUsed

    $("#pointsLeft").html(pointsLeft);
    $("#pointsUsed").html(pointsUsed);
}

function resetCCSkills() {
    $(skills).each(function(index, skill) {
        if (!(skill.allowed) && skill.skilled) {
            skill._setLevel(0);
            skill.levelDown();
        }
    })
}

function reset() {
    $(skills).each(function(index, skill) {
        skill._setLevel(1)
        skill.levelDown();
    });
    updateHash();
    updatePoints();
}

/*
function getImageBasedOnObjects() {
    object = {};
    $(skills).each(function(index, skill) {
        object[skill.skillId] = skill.currentLevel;
    });
    $.ajax({
        type: "POST",
        url: baseUrl + "/planner/create_image",
        data: JSON.stringify(object),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
    });
}*/

$(document).ready(function() { 
    // add html structure
    $(".skill").each(function(index, skill) {
        $(skill).append(`
        <div class="level-button level-button-minus"><i class="fas fa-xs fa-minus"></i></div>
        <div class="skill-icon-wrapper">
            <div class="skill-icon-effect-wrapper">
                <img src=${$(skill).attr("icon-src")}>
            </div>
            <span class="level">0</span>
        </div>
        <div class="level-button level-button-plus"><i class="fas fa-xs fa-plus"></i></div>
        `)
    });    

    // Create Skill Objects
    $(Object.keys(skillsBaseData)).each(function(index, skillId) {
        let skill = skillsBaseData[skillId];
        skills.push(new Skill(skillId, skill["max_level"], skill["relies_on"]))
    });

    // Hash 
    if (! location.hash) {
        // No hash given -> create a basic one
        updateHash();
        $(skills).each(function(index, skill) {
            skill.updateSkillDescription();
        });
    }
    else {
        updateObjectsBasedOnHash();
    }
    updateAllowedSkills();
    updatePoints()
    
    // Bindings
    $("#levelSelect").on("change", onLevelChange);
    $("#classSelect").on("change", onClassChange);

    $("#resetButton").on("click", reset);

    //$("#imageButton").on("click", getImageBasedOnObjects);

    if (isMobile) {
        $(".level-button-plus").click(mobileLevelUp);
        $(".level-button-minus").click(mobileLevelDown);
    }
    else {
        $(".level-button").css("visibility", "hidden"); // Does not move layout around
        $(".skill").on("contextmenu", event => event.preventDefault());
        $(".skill").on("mouseup", onSkillClick);
    }
});
