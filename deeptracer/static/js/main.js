/**
 * main.js - 入口 JS（Vue 初始化、Tab 切换、全局变量绑定）
 * 功能：
 * 1. 初始化Vue实例
 * 2. 处理Tab切换逻辑
 * 3. 绑定全局变量
 * 4. 处理代码Diff和Python Tutor逻辑
 */

console.log('Vue initializing...');

// 模拟数据兜底逻辑
const workflowDataValue = typeof workflow_data !== 'undefined' ? workflow_data : {
    'py_file_code': '# 测试代码\ndef hello():\n    print("Hello, World!")\n\nhello()',
    'original_code': 'def hello():\n    print("Hello")\n\nhello()',
    'modified_code': 'def hello():\n    print("Hello, World!")\n\nhello()',
    'modify_reason': '添加了", World!"字符串，使输出更完整'
};

const pyFileCodeValue = typeof py_file_code !== 'undefined' ? py_file_code : '# 测试代码\ndef hello():\n    print("Hello, World!")\n\nhello()';

const astHtmlValue = typeof ast_html !== 'undefined' ? ast_html : '<div style="padding: 20px; text-align: center;">AST可视化内容</div>';

const pyinstrumentHtmlValue = typeof pyinstrument_html !== 'undefined' ? pyinstrument_html : '<div style="padding: 20px; text-align: center;">Pyinstrument性能分析内容</div>';

console.log('workflowDataValue:', workflowDataValue);
console.log('pyFileCodeValue:', pyFileCodeValue);
console.log('astHtmlValue type:', typeof astHtmlValue, 'length:', astHtmlValue ? astHtmlValue.length : 0);
console.log('pyinstrumentHtmlValue type:', typeof pyinstrumentHtmlValue, 'length:', pyinstrumentHtmlValue ? pyinstrumentHtmlValue.length : 0);

new Vue({
    el: '#app',
    data: {
        // Tab配置
        tabs: [
            { name: 'diff-pytutor', label: 'Diff + PyTutor' },
            { name: 'ast', label: 'AST可视化' },
            { name: 'pyinstrument', label: 'Pyinstrument性能分析' }
        ],
        activeTab: 'diff-pytutor',
        
        // 工作流数据
        workflowData: workflowDataValue || {},
        
        // Python代码
        pyFileCode: pyFileCodeValue || '',
        
        // 编辑器代码
        editorCode: '',
        
        // AST和性能分析HTML
        astHtml: astHtmlValue || '',
        pyinstrumentHtml: pyinstrumentHtmlValue || '',
        
        // Diff结果
        diffResult: [],
        
        // 选择状态
        changeSelections: {},
        
        // 已确认的选择
        confirmedSelections: {},
        
        // 原因弹窗
        reasonDialogVisible: false,
        currentReason: '',
        
        // 编辑模式
        editMode: false
    },
    computed: {
        // Python Tutor URL
        pytutorUrl() {
            return generatePyTutorUrl(this.editorCode || this.pyFileCode);
        },
        
        // 是否所有修改行都已选择
        allChangesSelected() {
            for (let i = 0; i < this.diffResult.length; i++) {
                const line = this.diffResult[i];
                if (line.type !== 'unchanged' && !this.changeSelections[i]) {
                    return false;
                }
            }
            return true;
        },
        
        // 是否所有冲突都已确认
        allConflictsConfirmed() {
            for (let i = 0; i < this.diffResult.length; i++) {
                const line = this.diffResult[i];
                if (line.type !== 'unchanged' && !this.confirmedSelections[i]) {
                    return false;
                }
            }
            return true;
        }
    },
    mounted() {
        console.log('Vue mounted');
        // 初始化Diff结果
        this.initDiff();
        console.log('Diff initialized:', this.diffResult);
        console.log('All changes selected:', this.allChangesSelected);
    },
    methods: {
        // 初始化Diff
        initDiff() {
            console.log('initDiff called');
            console.log('workflowData:', this.workflowData);
            console.log('original_code:', this.workflowData.original_code);
            console.log('modified_code:', this.workflowData.modified_code);
            
            if (this.workflowData.original_code && this.workflowData.modified_code) {
                this.diffResult = generateDiff(
                    this.workflowData.original_code,
                    this.workflowData.modified_code
                );
                
                // 初始化选择状态
                this.initSelections();
            } else {
                console.error('workflowData missing original_code or modified_code');
            }
        },
        
        // 初始化选择状态
        initSelections() {
            this.changeSelections = {};
            this.confirmedSelections = {};
            for (let i = 0; i < this.diffResult.length; i++) {
                const line = this.diffResult[i];
                if (line.type === 'added') {
                    // 新增行默认选择不替换
                    this.changeSelections[i] = 'skip';
                } else if (line.type === 'deleted') {
                    // 删除行默认选择保留
                    this.changeSelections[i] = 'keep';
                } else if (line.type === 'modified') {
                    // 修改行默认选择保留修改后的代码
                    this.changeSelections[i] = 'keep_modified';
                }
            }
            console.log('初始化选择状态完成:', this.changeSelections);
        },
        
        // 处理选择变化
        onSelectionChange(index) {
            console.log(`第 ${index} 行选择变化：`, this.changeSelections[index]);
            console.log(`当前所有选择：`, JSON.parse(JSON.stringify(this.changeSelections)));
        },
        
        // 确认单行选择
        confirmSelection(index) {
            if (this.changeSelections[index]) {
                const selection = this.changeSelections[index];
                const line = this.diffResult[index];
                
                // 根据选择更新 diffResult
                if (line.type === 'modified') {
                    // 修改行：只保留选择的代码
                    if (selection === 'keep_modified') {
                        // 保留新代码，删除原代码
                        this.diffResult[index] = {
                            type: 'unchanged',
                            content: line.modifiedContent,
                            lineNumber: line.modifiedLineNum
                        };
                    } else {
                        // 保留原代码，删除新代码
                        this.diffResult[index] = {
                            type: 'unchanged',
                            content: line.originalContent,
                            lineNumber: line.originalLineNum
                        };
                    }
                } else if (line.type === 'deleted') {
                    // 删除行：如果选择删除，从 diffResult 中移除
                    if (selection === 'delete') {
                        this.diffResult.splice(index, 1);
                        // 重新索引后续的选择
                        this.reindexSelections(index);
                        return;
                    } else {
                        // 保留，改为未修改状态
                        this.diffResult[index].type = 'unchanged';
                    }
                } else if (line.type === 'added') {
                    // 新增行：如果选择不替换，从 diffResult 中移除
                    if (selection === 'skip') {
                        this.diffResult.splice(index, 1);
                        // 重新索引后续的选择
                        this.reindexSelections(index);
                        return;
                    } else {
                        // 替换，改为未修改状态
                        this.diffResult[index].type = 'unchanged';
                    }
                }
                
                // 记录已确认的选择
                this.$set(this.confirmedSelections, index, selection);
                console.log(`第 ${index} 行已确认选择：`, selection);
                this.$message.success('已确认该行选择');
            } else {
                this.$message.warning('请先选择操作');
            }
        },
        
        // 重新索引选择（删除行后需要调整索引）
        reindexSelections(deletedIndex) {
            const newChangeSelections = {};
            const newConfirmedSelections = {};
            
            for (let i = 0; i < this.diffResult.length; i++) {
                const oldIndex = i >= deletedIndex ? i + 1 : i;
                if (this.changeSelections[oldIndex]) {
                    newChangeSelections[i] = this.changeSelections[oldIndex];
                }
                if (this.confirmedSelections[oldIndex]) {
                    newConfirmedSelections[i] = this.confirmedSelections[oldIndex];
                }
            }
            
            this.changeSelections = newChangeSelections;
            this.confirmedSelections = newConfirmedSelections;
        },
        
        // 确认所有选择
        confirmAllSelections() {
            if (!this.allChangesSelected) {
                this.$message.warning('请先完成所有选择');
                return;
            }
            
            // 从后往前处理，避免索引问题
            const indices = [];
            for (let i = 0; i < this.diffResult.length; i++) {
                if (this.diffResult[i].type !== 'unchanged') {
                    indices.push(i);
                }
            }
            
            // 反向遍历，避免删除时索引错乱
            for (let i = indices.length - 1; i >= 0; i--) {
                const index = indices[i];
                const selection = this.changeSelections[index];
                const line = this.diffResult[index];
                
                // 根据选择更新 diffResult
                if (line.type === 'modified') {
                    if (selection === 'keep_modified') {
                        this.diffResult[index] = {
                            type: 'unchanged',
                            content: line.modifiedContent,
                            lineNumber: line.modifiedLineNum
                        };
                    } else {
                        this.diffResult[index] = {
                            type: 'unchanged',
                            content: line.originalContent,
                            lineNumber: line.originalLineNum
                        };
                    }
                    this.$set(this.confirmedSelections, index, selection);
                } else if (line.type === 'deleted') {
                    if (selection === 'delete') {
                        this.diffResult.splice(index, 1);
                    } else {
                        this.diffResult[index].type = 'unchanged';
                        this.$set(this.confirmedSelections, index, selection);
                    }
                } else if (line.type === 'added') {
                    if (selection === 'skip') {
                        this.diffResult.splice(index, 1);
                    } else {
                        this.diffResult[index].type = 'unchanged';
                        this.$set(this.confirmedSelections, index, selection);
                    }
                }
            }
            
            // 重新索引选择
            this.reindexSelections(0);
            
            console.log('所有选择已确认:', this.confirmedSelections);
            this.$message.success('所有选择已确认');
        },
        
        // 显示修改原因
        showModifyReason(index) {
            console.log('showModifyReason called with index:', index);
            this.currentReason = this.workflowData.modify_reason || '无修改原因';
            this.reasonDialogVisible = true;
            console.log('Reason dialog visible:', this.reasonDialogVisible);
        },
        
        // 复制合并后的代码
        copyMergedCode() {
            console.log('copyMergedCode called');
            if (!this.allConflictsConfirmed) {
                console.log('Not all conflicts confirmed');
                this.$message.warning('请先确认所有冲突的选择');
                return;
            }
            
            const mergedCode = mergeCode(this.diffResult, this.confirmedSelections);
            console.log('Merged code:', mergedCode);
            
            copyToClipboard(mergedCode)
                .then(() => {
                    console.log('Copy successful');
                    this.$message({
                        message: '复制成功！',
                        type: 'success'
                    });
                })
                .catch((error) => {
                    console.log('Copy failed:', error);
                    this.$message.error('复制失败，请手动复制');
                });
        },
        
        // 应用选择并进入编辑模式
        applySelections() {
            console.log('applySelections called');
            if (!this.allConflictsConfirmed) {
                console.log('Not all conflicts confirmed');
                this.$message.warning('请先确认所有冲突的选择');
                return;
            }
            
            const mergedCode = mergeCode(this.diffResult, this.confirmedSelections);
            console.log('Merged code:', mergedCode);
            this.editorCode = mergedCode;
            this.editMode = true;
            // 清空Diff结果，实现Diff消失的效果
            this.diffResult = [];
            console.log('Edit mode:', this.editMode);
            this.$message.success('已进入编辑模式');
        },
        
        // 应用编辑器代码到PyTutor
        applyEditorCode() {
            console.log('applyEditorCode called');
            if (!this.editorCode) {
                console.log('Editor code is empty');
                this.$message.warning('编辑器为空');
                return;
            }
            console.log('Editor code:', this.editorCode);
            this.$message.success('代码已更新到PyTutor');
        },
        
        // 退出编辑模式
        exitEditMode() {
            console.log('exitEditMode called');
            this.editMode = false;
            
            // 将编辑后的代码转换为 diffResult 格式显示
            if (this.editorCode) {
                const lines = this.editorCode.split('\n');
                this.diffResult = lines.map((line, index) => ({
                    type: 'unchanged',
                    content: line,
                    lineNumber: index + 1
                }));
            }
            
            console.log('Edit mode:', this.editMode);
            this.$message.info('已退出编辑模式，显示编辑后的代码');
        }
    }
});